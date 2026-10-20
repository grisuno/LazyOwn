/*
   Broadcom WPS Monitor identification rules.

   Scope: ELF32 ARM/MIPS Broadcom WPS monitor executables observed as
   wps_monitor, wpsmon, and live captured wpsmon variants.
*/

import "elf"

private rule Is_ELF32_ARM_or_MIPS
{
   condition:
      uint32(0) == 0x464c457f
      and uint8(4) == 1
      and (
         (uint8(5) == 1 and (uint16(0x12) == 0x0028 or uint16(0x12) == 0x0008))
         or
         (uint8(5) == 2 and (uint16be(0x12) == 0x0028 or uint16be(0x12) == 0x0008))
      )
}

rule BRCM_WPS_Monitor_Generic_ELF
{
   meta:
      description = "Detects generic Broadcom WPS monitor ELF32 ARM or MIPS executables across observed wps_monitor and wpsmon naming variants"
      author = "Quentin Kaiser <quentin@konkretesec.com>"
      date = "2026-07-27"
      score = 80
      tags = "Broadcom, WPS, ELF, ARM, MIPS"

   strings:
      $b1 = "<manufacturer>Broadcom Corporation</manufacturer>" ascii
      $b2 = "http://www.broadcom.com" ascii
      $b3 = "Broadcom_" ascii

      $m1 = "Usage: wps_monitor" ascii
      $m2 = "/tmp/wps_monitor.pid" ascii
      $m3 = "wps_proc_status" ascii
      $m4 = "wps_monitor" ascii
      $m5 = "ap_eap_sm_" ascii
      $m6 = "_wps_monitor_printf" ascii

      $p1 = "urn:schemas-wifialliance-org:device:WFADevice" ascii
      $p2 = "urn:schemas-wifialliance-org:service:WFAWLANConfig" ascii
      $p3 = "WFA-SimpleConfig-Enrollee-1-0" ascii
      $p4 = "WFA-SimpleConfig-Registrar-1-0" ascii
      $p5 = "WPS UPnP" ascii
      $p6 = "wps_processMsg" ascii

   condition:
      Is_ELF32_ARM_or_MIPS
      and (
         (1 of ($b*) and all of ($m1, $m2, $m3) and 2 of ($p1, $p2, $p3, $p4))
         or (2 of ($m*) and 1 of ($b*, $p*))
      )
}

rule BRCM_WPS_Monitor_HAL_Config_ELF
{
   meta:
      description = "Detects Broadcom WPS monitor ELF32 ARM or MIPS executables with the HAL WPS ER config event marker"
      author = "Quentin Kaiser <quentin@konkretesec.com>"
      date = "2026-08-03"
      score = 90
      tags = "Broadcom, WPS, HAL, ELF, ARM, MIPS"

   strings:
      $x1 = "Sending HAL_BCM_WIFI_WPS_ER_CONFIG event to WIFI AP" ascii

      $m1 = "Usage: wps_monitor" ascii
      $m2 = "/tmp/wps_monitor.pid" ascii
      $m3 = "wps_proc_status" ascii

      $p1 = "urn:schemas-wifialliance-org:device:WFADevice" ascii
      $p2 = "urn:schemas-wifialliance-org:service:WFAWLANConfig" ascii

   condition:
      Is_ELF32_ARM_or_MIPS
      and $x1
      and all of ($m*)
      and 1 of ($p*)
}

rule VULN_BRCM_WPS_EAP_Fragment_Reassembly_ELF
{
   meta:
      description = "Detects Broadcom WPS monitor ELF32 ARM or MIPS executables with a static vulnerable EAP-WPS fragment reassembly code shape"
      author = "Quentin Kaiser <quentin@konkretesec.com>"
      date = "2026-07-27"
      score = 95
      tags = "Broadcom, WPS, EAP, fragment-reassembly, ELF, ARM, MIPS"
      detector_scope = "Static vulnerable-code-shape detector; this is not proof that a specific live AP is exploitable"
      limitation = "Pure YARA cannot distinguish a patched build that preserves the exact vulnerable function bytes"

   strings:
      /*
         ap_eap_sm_process_sta_msg fragment path: WPS length is
         reduced by EAP_WPS_LF_OFFSET, checked against accumulated/declared
         receive state, then the reduced length is passed to memcpy.

         14 00 84 e2   add    r0, r4, #0x14
         18 70 01 e3   movw   r7, #0x1018
         ?? ?? ?? eb   bl     WpsNtohs helper
         0e 00 40 e2   sub    r0, r0, #0xe
         07 30 95 e7   ldr    r3, [r5, r7]
         08 10 95 e7   ldr    r1, [r5, r8]
         0e 20 43 e2   sub    r2, r3, #0xe
         00 20 82 e0   add    r2, r2, r0
         02 00 51 e1   cmp    r1, r2
         04 00 a0 33   movcc  r0, #4
         ?? ?? ?? 3a   bcc    reject/exit path
      */
      $arm_ap_eap_sm_process_sta_msg = {
         14 00 84 e2 18 70 01 e3 ?? ?? ?? eb
         ?? ?? ?? e5 0e 00 40 e2 ?? ?? ?? e7
         07 30 95 e7 08 10 95 e7 0e 20 43 e2
         00 20 82 e0 02 00 51 e1 04 00 a0 33
         ?? ?? ?? 3a
      }

      $arm_memcpy_sink = {
         /*
            07 00 95 e7   ldr    r0, [r5, r7]
            0e 10 81 e2   add    r1, r1, #0xe
            09 20 a0 e1   mov    r2, r9
            01 10 86 e0   add    r1, r6, r1
            81 0e 80 e2   add    r0, r0, #0x810
            00 00 85 e0   add    r0, r5, r0
            04 00 80 e2   add    r0, r0, #4
            ?? ?? ?? eb   bl     memcpy
            07 30 95 e7   ldr    r3, [r5, r7]
            03 00 89 e0   add    r0, r9, r3
            07 00 85 e7   str    r0, [r5, r7]
         */
         07 00 95 e7 0e 10 81 e2 09 20 a0 e1
         01 10 86 e0 81 0e 80 e2 00 00 85 e0
         04 00 80 e2 ?? ?? ?? eb 07 30 95 e7
         03 00 89 e0 07 00 85 e7
      }

      /*
         Retained vulnerable-function probe window. This is a
         static code-shape anchor, not a firmware-version or address test.

         3c 02 00 44   lui    v0, 0x44
         27 bd ff a8   addiu  sp, sp, -0x58
         8c 42 b7 10   lw     v0, -0x48f0(v0)
         af b4 00 4c   sw     s4, 0x4c(sp)
         af bf 00 54   sw     ra, 0x54(sp)
         af b5 00 50   sw     s5, 0x50(sp)
         af b3 00 48   sw     s3, 0x48(sp)
         af b2 00 44   sw     s2, 0x44(sp)
         af b1 00 40   sw     s1, 0x40(sp)
         af b0 00 3c   sw     s0, 0x3c(sp)
         00 80 a0 21   move   s4, a0
         10 40 01 ec   beqz   v0, later path
         8c 52 10 50   lw     s2, 0x1050(v0)
         8c 59 10 48   lw     t9, 0x1048(v0)
         13 20 01 ee   beqz   t9, later path
         24 02 10 09   addiu  v0, zero, 0x1009
      */
      $mips_vuln_window = {
         3c 02 00 44 27 bd ff a8 8c 42 b7 10 af b4 00 4c
         af bf 00 54 af b5 00 50 af b3 00 48 af b2 00 44
         af b1 00 40 af b0 00 3c 00 80 a0 21 10 40 01 ec
         8c 52 10 50 8c 59 10 48 13 20 01 ee 24 02 10 09
      }

      /*
         MIPS ap_eap_sm_process_sta_msg geometry: declared/accumulated
         state offsets 0x1014/0x1018, receive buffer offset 0x814, header copy,
         LF adjustment, dynamic receive-buffer memcpy, and accumulated update.

         8c 56 10 18   lw     s6, 0x1018(v0)
         8e 51 ?? ??   lw     s1, state pointer from s2-relative slot
         26 d6 ff f2   addiu  s6, s6, -0xe
         8e 22 10 14   lw     v0, 0x1014(s1)
         02 d5 18 21   addu   v1, s6, s5
         00 43 20 2b   sltu   a0, v0, v1

         8e 22 10 18   lw     v0, 0x1018(s1)
         26 24 08 14   addiu  a0, s1, 0x814
         02 60 28 21   move   a1, s3
         03 20 f8 09   jalr   t9
         24 06 00 0e   addiu  a2, zero, 0xe

         8e 24 10 18   lw     a0, 0x1018(s1)
         02 a3 a8 23   subu   s5, s5, v1
         24 84 08 14   addiu  a0, a0, 0x814
         02 65 28 21   addu   a1, s3, a1
         03 20 f8 09   jalr   t9
         02 a0 30 21   move   a2, s5
      */
      $mips_ap_eap_sm_process_sta_msg = {
         8c 56 10 18 8e 51 ?? ?? 26 d6 ff f2
         8e 22 10 14 02 d5 18 21 00 43 20 2b
         [0-64]
         8e 22 10 18 [0-24] 26 24 08 14
         02 60 28 21 03 20 f8 09 24 06 00 0e
         [0-48]
         8e 24 10 18 02 a3 a8 23 [0-24]
         24 84 08 14 02 65 28 21 03 20 f8 09
         02 a0 30 21
      }

      /*
         Compiler-independent immediate/field geometry. These fragments are
         deliberately combined as a family rather than used independently:
         two -14 operations, declared/accumulated length fields, and the fixed
         +0x814 receive-buffer geometry must all be present in the component.
      */
      $arm_sub_14 = { 0e ?? 4? e2 }
      $arm_movw_1014 = { 14 ?0 01 e3 }
      $arm_movw_1018 = { 18 ?0 01 e3 }
      $arm_add_1000 = { 01 ?? 8? e2 }
      $arm_ldr_14 = { 14 ?? 9? e5 }
      $arm_ldr_18 = { 18 ?? 9? e5 }
      $arm_add_810 = { 81 ?e 8? e2 }

      /* GCC -O0 helper variant with state offsets loaded from a literal pool. */
      $arm_o0_guard = {
         0e 30 43 e2 14 30 0b e5
         ?? 32 9f e5 30 10 1b e5 03 30 81 e0 00 20 93 e5
         ?? 32 9f e5 03 30 92 e7 0e 30 43 e2 10 30 0b e5
         [16-48]
         10 20 1b e5 14 30 1b e5 03 30 82 e0 03 00 51 e1
      }
      $arm_o0_sink = {
         81 2e 83 e2 04 20 82 e2
         [16-96]
         03 30 91 e7 03 00 82 e0
         [4-48]
         0e 20 83 e2 [8-48] ?? ?? ?? eb
      }

      $mips_be_declared = { (8? | a? | 24 | 26) ?? 10 14 }
      $mips_be_total = { (8? | a? | 24 | 26) ?? 10 18 }
      $mips_be_buffer = { (8? | a? | 24 | 26) ?? 08 14 }
      $mips_be_sub_14 = { 2? ?? ff f2 }

      $mips_le_declared = { 14 10 ?? (8? | a? | 24 | 26) }
      $mips_le_total = { 18 10 ?? (8? | a? | 24 | 26) }
      $mips_le_buffer = { 14 08 ?? (8? | a? | 24 | 26) }
      $mips_le_sub_14 = { f2 ff ?? 2? }

   condition:
      BRCM_WPS_Monitor_Generic_ELF
      and (
         (
            uint8(5) == 1
            and uint16(0x12) == 0x0028
            and (
               all of ($arm_ap_eap_sm_process_sta_msg, $arm_memcpy_sink)
               or all of ($arm_o0_guard, $arm_o0_sink)
               or for any i in (1..#arm_sub_14) : (
                  @arm_sub_14[i] % 4 == 0
                  and (
                     for any section in elf.sections : (
                        (section.flags & elf.SHF_EXECINSTR) != 0
                        and @arm_sub_14[i] >= section.offset
                        and @arm_sub_14[i] < section.offset + section.size
                     )
                     or for any segment in elf.segments : (
                        (segment.flags & elf.PF_X) != 0
                        and @arm_sub_14[i] >= segment.offset
                        and @arm_sub_14[i] < segment.offset + segment.file_size
                     )
                  )
                  and for 2 j in (1..#arm_sub_14) : (
                     @arm_sub_14[j] >= @arm_sub_14[i]
                     and @arm_sub_14[j] <= @arm_sub_14[i] + 0x1000
                  )
                  and for 2 j in (1..#arm_add_810) : (
                     @arm_add_810[j] >= @arm_sub_14[i]
                     and @arm_add_810[j] <= @arm_sub_14[i] + 0x1000
                  )
                  and (
                     (
                        $arm_movw_1014 in (@arm_sub_14[i]..@arm_sub_14[i] + 0x1000)
                        and $arm_movw_1018 in (@arm_sub_14[i]..@arm_sub_14[i] + 0x1000)
                     )
                     or (
                        $arm_add_1000 in (@arm_sub_14[i]..@arm_sub_14[i] + 0x1000)
                        and $arm_ldr_14 in (@arm_sub_14[i]..@arm_sub_14[i] + 0x1000)
                        and $arm_ldr_18 in (@arm_sub_14[i]..@arm_sub_14[i] + 0x1000)
                     )
                  )
               )
            )
         )
         or (
            uint8(5) == 2
            and uint16be(0x12) == 0x0008
            and (
               $mips_vuln_window
               or $mips_ap_eap_sm_process_sta_msg
               or for any i in (1..#mips_be_sub_14) : (
                  @mips_be_sub_14[i] % 4 == 0
                  and for 2 j in (1..#mips_be_sub_14) : (
                     @mips_be_sub_14[j] >= @mips_be_sub_14[i]
                     and @mips_be_sub_14[j] <= @mips_be_sub_14[i] + 0x1000
                  )
                  and $mips_be_declared in (@mips_be_sub_14[i]..@mips_be_sub_14[i] + 0x1000)
                  and $mips_be_total in (@mips_be_sub_14[i]..@mips_be_sub_14[i] + 0x1000)
                  and $mips_be_buffer in (@mips_be_sub_14[i]..@mips_be_sub_14[i] + 0x1000)
               )
            )
         )
         or (
            uint8(5) == 1
            and uint16(0x12) == 0x0008
            and for any i in (1..#mips_le_sub_14) : (
               @mips_le_sub_14[i] % 4 == 0
               and for 2 j in (1..#mips_le_sub_14) : (
                  @mips_le_sub_14[j] >= @mips_le_sub_14[i]
                  and @mips_le_sub_14[j] <= @mips_le_sub_14[i] + 0x1000
               )
               and $mips_le_declared in (@mips_le_sub_14[i]..@mips_le_sub_14[i] + 0x1000)
               and $mips_le_total in (@mips_le_sub_14[i]..@mips_le_sub_14[i] + 0x1000)
               and $mips_le_buffer in (@mips_le_sub_14[i]..@mips_le_sub_14[i] + 0x1000)
            )
         )
      )
}
