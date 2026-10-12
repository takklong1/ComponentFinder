import os

base = "ComponentFinder"

files = {
    "settings.gradle.kts": r'''pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "ComponentFinder"
include(":app")
''',

    "build.gradle.kts": r'''plugins {
    id("com.android.application") version "8.5.2" apply false
    id("org.jetbrains.kotlin.android") version "1.9.24" apply false
    id("org.jetbrains.kotlin.kapt") version "1.9.24" apply false
}
''',

    "gradle.properties": r'''org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
''',

    "app/build.gradle.kts": r'''plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.kapt")
}

android {
    namespace = "com.example.componentfinder"
    compileSdk = 34
    buildToolsVersion = "34.0.0"

    defaultConfig {
        applicationId = "com.example.componentfinder"
        minSdk = 26
        targetSdk = 34
        versionCode = 4
        versionName = "1.3"

        ndk {
            abiFilters.clear()
            abiFilters.add("arm64-v8a")
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
    buildFeatures { compose = true }
    composeOptions { kotlinCompilerExtensionVersion = "1.5.14" }
}

dependencies {
    implementation(platform("androidx.compose:compose-bom:2024.06.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.activity:activity-compose:1.9.0")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.3")
    implementation("androidx.navigation:navigation-compose:2.7.7")
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.documentfile:documentfile:1.0.1")

    implementation("com.google.mlkit:barcode-scanning:17.3.0")
    implementation("com.google.mlkit:text-recognition:16.0.1")
    implementation("androidx.camera:camera-camera2:1.3.4")
    implementation("androidx.camera:camera-lifecycle:1.3.4")
    implementation("androidx.camera:camera-view:1.3.4")

    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.8.1")

    implementation("androidx.room:room-runtime:2.6.1")
    implementation("androidx.room:room-ktx:2.6.1")
    kapt("androidx.room:room-compiler:2.6.1")
}
''',

    "app/proguard-rules.pro": r'''# 空文件即可
''',

    "app/src/main/AndroidManifest.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.CAMERA" />
    <uses-feature android:name="android.hardware.camera" android:required="false" />

    <application
        android:allowBackup="true"
        android:label="元件快查"
        android:supportsRtl="true"
        android:theme="@style/Theme.ComponentFinder">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:excludeFromRecents="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <activity
            android:name=".camera.CameraScanActivity"
            android:screenOrientation="portrait"
            android:excludeFromRecents="true"
            android:theme="@style/Theme.ComponentFinder" />

        <provider
            android:name="androidx.core.content.FileProvider"
            android:authorities="${applicationId}.fileprovider"
            android:exported="false"
            android:grantUriPermissions="true">
            <meta-data
                android:name="android.support.FILE_PROVIDER_PATHS"
                android:resource="@xml/file_paths" />
        </provider>

        <receiver
            android:name=".widget.ScanWidgetProvider"
            android:label="扫码"
            android:exported="true">
            <intent-filter>
                <action android:name="android.appwidget.action.APPWIDGET_UPDATE" />
            </intent-filter>
            <meta-data
                android:name="android.appwidget.provider"
                android:resource="@xml/scan_widget_info" />
        </receiver>

        <receiver
            android:name=".widget.OcrWidgetProvider"
            android:label="拍照识别"
            android:exported="true">
            <intent-filter>
                <action android:name="android.appwidget.action.APPWIDGET_UPDATE" />
            </intent-filter>
            <meta-data
                android:name="android.appwidget.provider"
                android:resource="@xml/ocr_widget_info" />
        </receiver>

        <receiver
            android:name=".widget.ConverterWidgetProvider"
            android:label="单位换算"
            android:exported="true">
            <intent-filter>
                <action android:name="android.appwidget.action.APPWIDGET_UPDATE" />
            </intent-filter>
            <meta-data
                android:name="android.appwidget.provider"
                android:resource="@xml/converter_widget_info" />
        </receiver>
    </application>
</manifest>
''',

    "app/src/main/res/values/strings.xml": r'''<resources>
    <string name="app_name">元件快查</string>
</resources>
''',

    "app/src/main/res/values/themes.xml": r'''<resources>
    <style name="Theme.ComponentFinder" parent="android:Theme.Material.Light.NoActionBar" />
</resources>
''',

    "app/src/main/res/xml/file_paths.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<paths>
    <cache-path name="cache" path="." />
</paths>
''',

    "app/src/main/res/xml/scan_widget_info.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<appwidget-provider xmlns:android="http://schemas.android.com/apk/res/android"
    android:minWidth="40dp"
    android:minHeight="40dp"
    android:targetCellWidth="1"
    android:targetCellHeight="1"
    android:updatePeriodMillis="0"
    android:initialLayout="@layout/widget_scan"
    android:resizeMode="none"
    android:widgetCategory="home_screen" />
''',

    "app/src/main/res/xml/ocr_widget_info.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<appwidget-provider xmlns:android="http://schemas.android.com/apk/res/android"
    android:minWidth="40dp"
    android:minHeight="40dp"
    android:targetCellWidth="1"
    android:targetCellHeight="1"
    android:updatePeriodMillis="0"
    android:initialLayout="@layout/widget_ocr"
    android:resizeMode="none"
    android:widgetCategory="home_screen" />
''',

    "app/src/main/res/xml/converter_widget_info.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<appwidget-provider xmlns:android="http://schemas.android.com/apk/res/android"
    android:minWidth="40dp"
    android:minHeight="40dp"
    android:targetCellWidth="1"
    android:targetCellHeight="1"
    android:updatePeriodMillis="0"
    android:initialLayout="@layout/widget_converter"
    android:resizeMode="none"
    android:widgetCategory="home_screen" />
''',

    "app/src/main/res/layout/widget_scan.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/widget_root"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:background="#FF5722"
    android:padding="4dp">
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="扫码"
        android:textColor="#FFFFFF"
        android:textSize="14sp"
        android:textStyle="bold" />
</LinearLayout>
''',

    "app/src/main/res/layout/widget_ocr.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/widget_root"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:background="#2196F3"
    android:padding="4dp">
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="拍照识别"
        android:textColor="#FFFFFF"
        android:textSize="11sp"
        android:textStyle="bold" />
</LinearLayout>
''',

    "app/src/main/res/layout/widget_converter.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/widget_root"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:background="#4CAF50"
    android:padding="4dp">
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="换算"
        android:textColor="#FFFFFF"
        android:textSize="14sp"
        android:textStyle="bold" />
</LinearLayout>
''',

    "app/src/main/assets/rules.json": r'''[
  {
    "brand": "YAGEO",
    "type": "电容",
    "pattern": "^CC(0603|0805|1206)([A-Z]{2})(NPO|X7R|X5R)([0-9A-Z]{3})(\\d{3})$",
    "packageGroup": 1, "toleranceGroup": 2, "materialGroup": 3,
    "voltageGroup": 4, "valueGroup": 5
  },
  {
    "brand": "YAGEO",
    "type": "电阻",
    "pattern": "^RC(0603|0805|1206)([A-Z]{2})-?(\\d{2})([0-9A-Z]{3,4})$",
    "packageGroup": 1, "toleranceGroup": 2, "valueGroup": 4,
    "voltageGroup": -1, "materialGroup": -1
  },
  {
    "brand": "SAMSUNG",
    "type": "电容",
    "pattern": "^CL(03|05|10|21|31|43)([A-Z])(\\d{3})([A-Z])([0-9A-Z])(\\d)([A-Z]{3})$",
    "packageGroup": 1, "materialGroup": 2, "valueGroup": 3,
    "toleranceGroup": 4, "voltageGroup": 5
  },
  {
    "brand": "MURATA",
    "type": "电容",
    "pattern": "^GRM(\\d{2})([A-Z0-9]{2})([A-Z0-9])([0-9A-Z]{2})(\\d{3})([A-Z])([A-Z0-9]{2})([A-Z0-9])$",
    "packageGroup": 1, "materialGroup": 3, "voltageGroup": 4,
    "valueGroup": 5, "toleranceGroup": 6
  },
  {
    "brand": "TDK",
    "type": "电容",
    "pattern": "^C(0603|1005|1608|2012|3216|3225|4532|5750)(X7R|X5R|C0G|NPO|Y5V|X7S)([0-9A-Z]{2})(\\d{3})([A-Z])([A-Z0-9]{3})$",
    "packageGroup": 1, "materialGroup": 2, "voltageGroup": 3,
    "valueGroup": 4, "toleranceGroup": 5
  },
  {
    "brand": "CCTC",
    "type": "电容",
    "pattern": "^TCC(0603|0805|1206)(X7R|X5R|NPO|C0G)(\\d{3})([A-Z])(\\d{3})([A-Z]{2})$",
    "packageGroup": 1, "materialGroup": 2, "valueGroup": 3,
    "toleranceGroup": 4, "voltageGroup": 5
  },
  {
    "brand": "FH",
    "type": "电容",
    "pattern": "^(0603|0805|1206)([A-Z]{1,2})(\\d{3})([A-Z])(\\d{3})(NT)$",
    "packageGroup": 1, "materialGroup": 2, "valueGroup": 3,
    "toleranceGroup": 4, "voltageGroup": 5
  }
]
''',

    "app/src/main/java/com/example/componentfinder/MainActivity.kt": r'''package com.example.componentfinder

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.example.componentfinder.ui.navigation.AppNav
import com.example.componentfinder.ui.theme.ComponentFinderTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val openConverter = intent.getBooleanExtra("open_converter", false)
        setContent {
            ComponentFinderTheme {
                AppNav(startDestination = if (openConverter) "converter" else "home")
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        if (isFinishing && !isChangingConfigurations) {
            android.os.Process.killProcess(android.os.Process.myPid())
        }
    }
}
''',

    "app/src/main/java/com/example/componentfinder/domain/model/ComponentSpec.kt": r'''package com.example.componentfinder.domain.model

data class ComponentSpec(
    val type: String,
    val packageName: String,
    val value: String,
    val tolerance: String,
    val voltage: String,
    val quantity: String,
    val material: String,
    val brand: String
) {
    fun toOrderedList(): List<Pair<String, String>> = listOf(
        "封装" to packageName,
        "容值/阻值" to value,
        "精度" to tolerance,
        "电压" to voltage,
        "数量" to quantity,
        "材质" to material,
        "品牌" to brand
    )
}
''',

    "app/src/main/java/com/example/componentfinder/domain/model/Rule.kt": r'''package com.example.componentfinder.domain.model

data class Rule(
    val brand: String,
    val type: String,
    val pattern: Regex,
    val packageGroup: Int = -1,
    val valueGroup: Int = -1,
    val toleranceGroup: Int = -1,
    val voltageGroup: Int = -1,
    val materialGroup: Int = -1
)
''',

    "app/src/main/java/com/example/componentfinder/domain/parser/CodeMaps.kt": r'''package com.example.componentfinder.domain.parser

object CodeMaps {

    fun capValue(code: String): String {
        val c = code.uppercase().replace(" ", "")
        if (c == "-" || c.isEmpty()) return "-"
        if (c.matches(Regex("\\d{3}"))) {
            val base = c.substring(0, 2).toInt()
            val mult = c.substring(2).toInt()
            return formatCap(base * Math.pow(10.0, mult.toDouble()))
        }
        val m = Regex("^(\\d+)([PNU])(\\d*)$").find(c)
        if (m != null) {
            val (num, unit, extra) = m.destructured
            val base = if (extra.isNotEmpty()) "$num.$extra".toDouble() else num.toDouble()
            val pf = when (unit) {
                "P" -> base
                "N" -> base * 1000
                "U" -> base * 1_000_000
                else -> base
            }
            return formatCap(pf)
        }
        return c
    }

    private fun formatCap(pf: Double): String {
        val v = round(pf)
        return when {
            v >= 1_000_000 -> "${trim(v / 1_000_000)} µF"
            v >= 1000 -> "${trim(v / 1000)} nF"
            else -> "${trim(v)} pF"
        }
    }

    fun resValue(code: String): String {
        val c = code.uppercase().replace(" ", "")
        if (c == "-" || c.isEmpty()) return "-"
        if (c.matches(Regex("\\d{3,4}"))) {
            val digits = c.length
            val base = if (digits == 3) c.substring(0, 2).toInt() else c.substring(0, 3).toInt()
            val mult = c.last().toString().toInt()
            return formatRes(base * Math.pow(10.0, mult.toDouble()))
        }
        val m = Regex("^(\\d+)([RKM])(\\d*)$").find(c)
        if (m != null) {
            val (num, unit, extra) = m.destructured
            val base = if (extra.isNotEmpty()) "$num.$extra".toDouble() else num.toDouble()
            val ohm = when (unit) {
                "R" -> base
                "K" -> base * 1000
                "M" -> base * 1_000_000
                else -> base
            }
            return formatRes(ohm)
        }
        if (c.length > 4) {
            val trimmed = c.substring(0, 4)
            if (trimmed != c) return resValue(trimmed)
        }
        if (c == "0R" || c == "0") return "0Ω"
        return c
    }

    private fun formatRes(ohm: Double): String {
        val v = round(ohm)
        return when {
            v >= 1_000_000 -> "${trim(v / 1_000_000)} MΩ"
            v >= 1000 -> "${trim(v / 1000)} kΩ"
            else -> "${trim(v)} Ω"
        }
    }

    fun voltage(code: String): String {
        val c = code.uppercase().replace(" ", "")
        if (c == "-" || c.isEmpty()) return "-"
        return when (c) {
            "9BN", "9BB", "B8", "500", "1H", "A" -> "50V"
            "0BN", "OBN", "0BB", "OBB", "8BB", "1E", "X", "T" -> "25V"
            "7BB", "1C", "Y", "J" -> "16V"
            "5BB", "0J" -> "6.3V"
            "C8", "101", "2A", "1", "B" -> "100V"
            "2E", "251" -> "250V"
            "2J", "L" -> "630V"
            "102", "1K", "3A" -> "1000V"
            "451" -> "450V"
            "160" -> "16V"
            "250" -> "25V"
            "Z" -> "10V"
            "3" -> "25V"
            "5" -> "50V"
            "E" -> "500V"
            else -> c
        }
    }

    fun material(code: String): String {
        val c = code.uppercase().replace(" ", "")
        if (c == "-" || c.isEmpty()) return "-"
        return when {
            c.contains("NPO") || c.contains("C0G") || c.contains("CG") -> "NPO (C0G)"
            c.contains("X7R") -> "X7R"
            c.contains("X7S") -> "X7S"
            c.contains("X7T") -> "X7T"
            c.contains("X6S") -> "X6S"
            c.contains("X6T") -> "X6T"
            c.contains("X5R") -> "X5R"
            c.contains("Y5V") -> "Y5V"
            else -> c
        }
    }

    fun tolerance(code: String): String {
        val c = code.uppercase().replace(" ", "")
        if (c == "-" || c.isEmpty()) return "-"
        val key = if (c.length >= 2 && c[0] in "JKMFGBCDZ") c[0].toString() else c
        return when (key) {
            "J" -> "±5%"
            "K" -> "±10%"
            "M" -> "±20%"
            "F" -> "±1%"
            "G" -> "±2%"
            "B" -> "±0.1%"
            "C" -> "±0.25%"
            "D" -> "±0.5%"
            "Z" -> "+80%/-20%"
            else -> c
        }
    }

    private fun round(v: Double): Double = Math.round(v * 1000.0) / 1000.0

    private fun trim(v: Double): String {
        val r = round(v)
        return if (r == r.toLong().toDouble()) r.toLong().toString() else r.toString()
    }
}
''',

    "app/src/main/java/com/example/componentfinder/domain/parser/SMDCodeParser.kt": r'''package com.example.componentfinder.domain.parser

import com.example.componentfinder.domain.model.ComponentSpec

object SMDCodeParser {

    private val E96_BASE_VALUES = mapOf(
        "01" to 100.0, "02" to 102.0, "03" to 105.0, "04" to 107.0, "05" to 110.0,
        "06" to 113.0, "07" to 115.0, "08" to 118.0, "09" to 121.0, "10" to 124.0,
        "11" to 127.0, "12" to 130.0, "13" to 133.0, "14" to 137.0, "15" to 140.0,
        "16" to 143.0, "17" to 147.0, "18" to 150.0, "19" to 154.0, "20" to 158.0,
        "21" to 162.0, "22" to 165.0, "23" to 169.0, "24" to 174.0, "25" to 178.0,
        "26" to 182.0, "27" to 187.0, "28" to 191.0, "29" to 196.0, "30" to 200.0,
        "31" to 205.0, "32" to 210.0, "33" to 215.0, "34" to 221.0, "35" to 226.0,
        "36" to 232.0, "37" to 237.0, "38" to 243.0, "39" to 249.0, "40" to 255.0,
        "41" to 261.0, "42" to 267.0, "43" to 274.0, "44" to 280.0, "45" to 287.0,
        "46" to 294.0, "47" to 301.0, "48" to 309.0, "49" to 316.0, "50" to 324.0,
        "51" to 332.0, "52" to 340.0, "53" to 348.0, "54" to 357.0, "55" to 365.0,
        "56" to 374.0, "57" to 383.0, "58" to 392.0, "59" to 402.0, "60" to 412.0,
        "61" to 422.0, "62" to 432.0, "63" to 442.0, "64" to 453.0, "65" to 464.0,
        "66" to 475.0, "67" to 487.0, "68" to 499.0, "69" to 511.0, "70" to 523.0,
        "71" to 536.0, "72" to 549.0, "73" to 562.0, "74" to 576.0, "75" to 590.0,
        "76" to 604.0, "77" to 619.0, "78" to 634.0, "79" to 649.0, "80" to 665.0,
        "81" to 681.0, "82" to 698.0, "83" to 715.0, "84" to 732.0, "85" to 750.0,
        "86" to 768.0, "87" to 787.0, "88" to 806.0, "89" to 825.0, "90" to 845.0,
        "91" to 866.0, "92" to 887.0, "93" to 909.0, "94" to 931.0, "95" to 953.0,
        "96" to 976.0
    )

    private val E96_MULTIPLIERS = mapOf(
        "Z" to -3, "Y" to -2, "R" to -1, "X" to -1,
        "A" to 0, "B" to 1, "C" to 2, "D" to 3, "E" to 4, "F" to 5,
        "G" to 6, "H" to 7, "I" to 8, "J" to 9
    )

    fun parseAll(input: String): List<ComponentSpec> {
        val clean = input.trim().uppercase().replace(" ", "").replace("-", "")
        val results = mutableListOf<ComponentSpec>()
        parseCapacitor(clean)?.let { results.add(it) }
        parseResistor(clean)?.let { results.add(it) }
        return results
    }

    private fun parseCapacitor(code: String): ComponentSpec? {
        Regex("^(\\d{3})$").find(code)?.let { m ->
            val value = m.groupValues[1]
            val pf = value.substring(0, 2).toDouble() * Math.pow(10.0, value.substring(2).toInt())
            return ComponentSpec(
                type = "电容",
                packageName = "未知",
                value = formatCapacitance(pf),
                tolerance = "常见 ±5% (J) / ±10% (K) / ±20% (M)",
                voltage = "需结合封装",
                quantity = "-",
                material = "需结合完整型号",
                brand = "通用丝印"
            )
        }
        return null
    }

    private fun parseResistor(code: String): ComponentSpec? {
        Regex("^(\\d{4})$").find(code)?.let { m ->
            val value = m.groupValues[1]
            val base = value.substring(0, 3).toDouble()
            val mult = value.substring(3).toInt()
            val ohm = base * Math.pow(10.0, mult.toDouble())
            return ComponentSpec(
                type = "电阻",
                packageName = "未知",
                value = formatResistance(ohm),
                tolerance = "±1% (E96系列)",
                voltage = "-",
                quantity = "-",
                material = "厚膜",
                brand = "E96 数值表示"
            )
        }

        Regex("^(\\d{3})$").find(code)?.let { m ->
            val value = m.groupValues[1]
            val base = value.substring(0, 2).toDouble()
            val mult = value.substring(2).toInt()
            val ohm = base * Math.pow(10.0, mult.toDouble())
            return ComponentSpec(
                type = "电阻",
                packageName = "未知",
                value = formatResistance(ohm),
                tolerance = "±5% (E24系列)",
                voltage = "-",
                quantity = "-",
                material = "厚膜",
                brand = "E24 数值表示"
            )
        }

        Regex("^(\\d{2})([A-Z])$").find(code)?.let { m ->
            val baseCode = m.groupValues[1]
            val multCode = m.groupValues[2]
            val baseValue = E96_BASE_VALUES[baseCode] ?: return null
            val mult = E96_MULTIPLIERS[multCode] ?: return null
            val ohm = baseValue * Math.pow(10.0, mult.toDouble())
            return ComponentSpec(
                type = "电阻",
                packageName = "常见0603",
                value = formatResistance(ohm),
                tolerance = "±1% (E96系列)",
                voltage = "-",
                quantity = "-",
                material = "厚膜",
                brand = "E96 代码表示"
            )
        }

        return null
    }

    private fun formatCapacitance(pf: Double): String {
        return when {
            pf >= 1_000_000 -> "${formatNumber(pf / 1_000_000)} µF"
            pf >= 1000 -> "${formatNumber(pf / 1000)} nF"
            else -> "${formatNumber(pf)} pF"
        }
    }

    private fun formatResistance(ohm: Double): String {
        return when {
            ohm >= 1_000_000 -> "${formatNumber(ohm / 1_000_000)} MΩ"
            ohm >= 1000 -> "${formatNumber(ohm / 1000)} kΩ"
            else -> "${formatNumber(ohm)} Ω"
        }
    }

    private fun formatNumber(num: Double): String {
        val rounded = Math.round(num * 1000.0) / 1000.0
        return if (rounded == rounded.toLong().toDouble()) {
            rounded.toLong().toString()
        } else {
            rounded.toString()
        }
    }
}
''',

    "app/src/main/java/com/example/componentfinder/domain/parser/GenericParser.kt": r'''package com.example.componentfinder.domain.parser

import com.example.componentfinder.domain.model.ComponentSpec

object GenericParser {
    fun parse(input: String): ComponentSpec? = null
}
''',

    "app/src/main/java/com/example/componentfinder/domain/parser/ParserEngine.kt": r'''package com.example.componentfinder.domain.parser

import com.example.componentfinder.domain.model.ComponentSpec
import com.example.componentfinder.domain.model.Rule

class ParserEngine(private val rules: List<Rule>) {

    fun parseAll(input: String): List<ComponentSpec> {
        val clean = input.trim().uppercase()
            .replace(" ", "").replace("\n", "").replace("\t", "")
        val results = LinkedHashSet<ComponentSpec>()

        for (rule in rules) {
            rule.pattern.matchEntire(clean)?.let {
                results.add(buildSpec(rule, it))
            }
        }
        if (results.isNotEmpty()) return results.toList()

        for (candidate in extractCandidates(clean)) {
            for (rule in rules) {
                rule.pattern.matchEntire(candidate)?.let {
                    results.add(buildSpec(rule, it))
                }
            }
        }
        if (results.isNotEmpty()) return results.toList()

        SMDCodeParser.parseAll(clean).forEach { results.add(it) }

        GenericParser.parse(clean)?.let { results.add(it) }

        return results.toList()
    }

    fun parse(input: String): ComponentSpec? = parseAll(input).firstOrNull()

    private fun buildSpec(rule: Rule, match: MatchResult): ComponentSpec {
        val rawValue = group(match, rule.valueGroup)
        val rawTol = group(match, rule.toleranceGroup)
        val rawVolt = group(match, rule.voltageGroup)
        val rawMat = group(match, rule.materialGroup)

        return ComponentSpec(
            type = rule.type,
            packageName = group(match, rule.packageGroup),
            value = if (rule.type == "电阻") CodeMaps.resValue(rawValue) else CodeMaps.capValue(rawValue),
            tolerance = CodeMaps.tolerance(rawTol),
            voltage = CodeMaps.voltage(rawVolt),
            quantity = "-",
            material = CodeMaps.material(rawMat),
            brand = rule.brand
        )
    }

    private fun group(match: MatchResult, index: Int): String {
        if (index <= 0) return "-"
        return match.groupValues.getOrNull(index)?.ifEmpty { "-" } ?: "-"
    }

    private fun extractCandidates(text: String): List<String> {
        val result = mutableListOf<String>()
        Regex("CC\\d{4}[A-Z]{2}(?:NPO|X7R|X5R)[0-9A-Z]{3}\\d{3}").findAll(text).forEach { result.add(it.value) }
        Regex("RC\\d{4}[A-Z]{2}-?\\d{2}[0-9A-Z]{3,4}").findAll(text).forEach { result.add(it.value) }
        Regex("CL\\d{2}[A-Z]\\d{3}[A-Z][0-9A-Z]{2}[A-Z]{3}").findAll(text).forEach { result.add(it.value) }
        Regex("TCC\\d{4}(?:X7R|X5R|NPO|C0G)\\d{3}[A-Z]\\d{3}[A-Z]{2}").findAll(text).forEach { result.add(it.value) }
        Regex("GRM\\d{2}[A-Z0-9]{3}[0-9A-Z]{2}\\d{3}[A-Z][A-Z0-9]{2}[A-Z0-9]").findAll(text).forEach { result.add(it.value) }
        Regex("C\\d{4}(?:X7R|X5R|C0G|NPO|Y5V|X7S)[0-9A-Z]{2}\\d{3}[A-Z][A-Z0-9]{3}").findAll(text).forEach { result.add(it.value) }
        Regex("\\d{4}[A-Z]{1,2}\\d{3}[A-Z]\\d{3}[A-Z]{2}").findAll(text).forEach { result.add(it.value) }
        return result
    }
}
''',

    "app/src/main/java/com/example/componentfinder/domain/parser/UnitConverter.kt": r'''package com.example.componentfinder.domain.parser

object UnitConverter {
    fun pfToNf(pf: Double) = pf / 1000
    fun nfToUf(nf: Double) = nf / 1000
    fun ufToNf(uf: Double) = uf * 1000
    fun nfToPf(nf: Double) = nf * 1000
    fun ohmToKohm(ohm: Double) = ohm / 1000
    fun kohmToMohm(kohm: Double) = kohm / 1000
}
''',

    "app/src/main/java/com/example/componentfinder/data/RulesRepository.kt": r'''package com.example.componentfinder.data

import android.content.Context
import com.example.componentfinder.domain.model.Rule
import org.json.JSONArray

class RulesRepository(private val context: Context) {
    fun loadRules(): List<Rule> {
        val json = context.assets.open("rules.json").bufferedReader().use { it.readText() }
        val arr = JSONArray(json)
        val rules = mutableListOf<Rule>()
        for (i in 0 until arr.length()) {
            val obj = arr.getJSONObject(i)
            rules.add(
                Rule(
                    brand = obj.getString("brand"),
                    type = obj.getString("type"),
                    pattern = Regex(obj.getString("pattern")),
                    packageGroup = obj.optInt("packageGroup", -1),
                    valueGroup = obj.optInt("valueGroup", -1),
                    toleranceGroup = obj.optInt("toleranceGroup", -1),
                    voltageGroup = obj.optInt("voltageGroup", -1),
                    materialGroup = obj.optInt("materialGroup", -1)
                )
            )
        }
        return rules
    }
}
''',

    "app/src/main/java/com/example/componentfinder/data/db/HistoryEntity.kt": r'''package com.example.componentfinder.data.db

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "history")
data class HistoryEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val model: String,
    val packageName: String,
    val value: String,
    val tolerance: String,
    val voltage: String,
    val quantity: String,
    val material: String,
    val brand: String,
    val timestamp: Long = System.currentTimeMillis()
)
''',

    "app/src/main/java/com/example/componentfinder/data/db/HistoryDao.kt": r'''package com.example.componentfinder.data.db

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface HistoryDao {
    @Insert
    suspend fun insert(entity: HistoryEntity)

    @Query("SELECT * FROM history ORDER BY timestamp DESC LIMIT 200")
    fun getAll(): Flow<List<HistoryEntity>>

    @Query("DELETE FROM history")
    suspend fun clearAll()
}
''',

    "app/src/main/java/com/example/componentfinder/data/db/AppDatabase.kt": r'''package com.example.componentfinder.data.db

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase

@Database(entities = [HistoryEntity::class], version = 1, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun historyDao(): HistoryDao

    companion object {
        @Volatile private var INSTANCE: AppDatabase? = null
        fun get(context: Context): AppDatabase =
            INSTANCE ?: synchronized(this) {
                INSTANCE ?: Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "component_finder.db"
                ).build().also { INSTANCE = it }
            }
    }
}
''',

    "app/src/main/java/com/example/componentfinder/data/HistoryRepository.kt": r'''package com.example.componentfinder.data

import android.content.Context
import com.example.componentfinder.data.db.AppDatabase
import com.example.componentfinder.data.db.HistoryEntity
import com.example.componentfinder.domain.model.ComponentSpec

class HistoryRepository(context: Context) {
    private val dao = AppDatabase.get(context).historyDao()

    suspend fun save(model: String, spec: ComponentSpec) {
        dao.insert(
            HistoryEntity(
                model = model,
                packageName = spec.packageName,
                value = spec.value,
                tolerance = spec.tolerance,
                voltage = spec.voltage,
                quantity = spec.quantity,
                material = spec.material,
                brand = spec.brand
            )
        )
    }

    fun getAll() = dao.getAll()
    suspend fun clear() = dao.clearAll()
}
''',

    "app/src/main/java/com/example/componentfinder/util/PermissionUtil.kt": r'''package com.example.componentfinder.util

import android.Manifest
import android.content.pm.PackageManager
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.runtime.*
import androidx.compose.ui.platform.LocalContext
import androidx.core.content.ContextCompat

@Composable
fun rememberCameraPermissionState(): Pair<Boolean, () -> Unit> {
    val context = LocalContext.current
    var granted by remember {
        mutableStateOf(
            ContextCompat.checkSelfPermission(
                context, Manifest.permission.CAMERA
            ) == PackageManager.PERMISSION_GRANTED
        )
    }
    val launcher = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted = it }
    return granted to { launcher.launch(Manifest.permission.CAMERA) }
}
''',

    "app/src/main/java/com/example/componentfinder/util/ModelExtractor.kt": r'''package com.example.componentfinder.util

object ModelExtractor {

    private val fullModelPatterns = listOf(
        Regex("CC\\d{4}[A-Z]{2}(?:NPO|X7R|X5R)[0-9A-Z]{3}\\d{3}"),
        Regex("RC\\d{4}[A-Z]{2}-?\\d{2}[0-9A-Z]{3,4}"),
        Regex("CL\\d{2}[A-Z]\\d{3}[A-Z][0-9A-Z]{2}[A-Z]{3}"),
        Regex("TCC\\d{4}(?:X7R|X5R|NPO|C0G)\\d{3}[A-Z]\\d{3}[A-Z]{2}"),
        Regex("GRM\\d{2}[A-Z0-9]{3}[0-9A-Z]{2}\\d{3}[A-Z][A-Z0-9]{2}[A-Z0-9]"),
        Regex("C\\d{4}(?:X7R|X5R|C0G|NPO|Y5V|X7S)[0-9A-Z]{2}\\d{3}[A-Z][A-Z0-9]{3}"),
        Regex("\\d{4}[A-Z]{1,2}\\d{3}[A-Z]\\d{3}[A-Z]{2}"),
        Regex("\\d{4}[A-Z]\\d[A-Z]\\d{4}[A-Z0-9]+")
    )

    fun extractAll(text: String): List<String> {
        val candidates = LinkedHashSet<String>()
        val upper = text.uppercase()

        val lines = upper.split(Regex("[\\r\\n]+"))
        for (line in lines) {
            val compact = line.replace(" ", "")
            for (p in fullModelPatterns) {
                p.find(compact)?.let { candidates.add(it.value) }
            }
        }

        if (candidates.isEmpty()) {
            val compact = upper.replace(" ", "").replace("\n", "").replace("\t", "")
            for (p in fullModelPatterns) {
                p.findAll(compact).forEach { candidates.add(it.value) }
            }
        }

        if (candidates.isEmpty()) {
            for (line in lines) {
                val compact = line.replace(" ", "").trim()
                if (compact.length in 3..5) {
                    if (compact.matches(Regex("^\\d{3,4}$")) ||
                        compact.matches(Regex("^\\d{2}[A-Z]$")) ||
                        compact.matches(Regex("^\\d+[Rr]\\d+$"))) {
                        candidates.add(compact)
                    }
                }
            }
        }

        return candidates.toList()
    }

    fun extract(text: String): String? = extractAll(text).firstOrNull()
}
''',

    "app/src/main/java/com/example/componentfinder/camera/BarcodeAnalyzer.kt": r'''package com.example.componentfinder.camera

import android.annotation.SuppressLint
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageProxy
import com.google.mlkit.vision.barcode.BarcodeScanning
import com.google.mlkit.vision.common.InputImage

class BarcodeAnalyzer(
    private val onResult: (String) -> Unit
) : ImageAnalysis.Analyzer {

    private val scanner = BarcodeScanning.getClient()

    @SuppressLint("UnsafeOptInUsageError")
    override fun analyze(imageProxy: ImageProxy) {
        val mediaImage = imageProxy.image ?: run {
            imageProxy.close(); return
        }
        val image = InputImage.fromMediaImage(
            mediaImage, imageProxy.imageInfo.rotationDegrees
        )
        scanner.process(image)
            .addOnSuccessListener { barcodes ->
                barcodes.firstOrNull { it.rawValue != null }?.let {
                    onResult(it.rawValue!!)
                }
            }
            .addOnCompleteListener { imageProxy.close() }
    }
}
''',

    "app/src/main/java/com/example/componentfinder/camera/TextAnalyzer.kt": r'''package com.example.componentfinder.camera

import android.annotation.SuppressLint
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageProxy
import com.google.mlkit.vision.common.InputImage
import com.google.mlkit.vision.text.TextRecognition
import com.google.mlkit.vision.text.latin.TextRecognizerOptions

class TextAnalyzer(
    private val onResult: (String) -> Unit
) : ImageAnalysis.Analyzer {

    private val recognizer =
        TextRecognition.getClient(TextRecognizerOptions.DEFAULT_OPTIONS)

    @SuppressLint("UnsafeOptInUsageError")
    override fun analyze(imageProxy: ImageProxy) {
        val mediaImage = imageProxy.image ?: run {
            imageProxy.close(); return
        }
        val image = InputImage.fromMediaImage(
            mediaImage, imageProxy.imageInfo.rotationDegrees
        )
        recognizer.process(image)
            .addOnSuccessListener { onResult(it.text) }
            .addOnCompleteListener { imageProxy.close() }
    }
}
''',

    "app/src/main/java/com/example/componentfinder/camera/CameraPreview.kt": r'''package com.example.componentfinder.camera

import android.util.Size
import androidx.camera.core.*
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLifecycleOwner
import androidx.compose.ui.viewinterop.AndroidView
import androidx.core.content.ContextCompat
import java.util.concurrent.Executors

enum class AnalyzerMode { BARCODE, OCR }

@Composable
fun CameraPreview(
    modifier: Modifier = Modifier,
    analyzerMode: AnalyzerMode,
    onCodeDetected: (String) -> Unit
) {
    val context = LocalContext.current
    val lifecycleOwner = LocalLifecycleOwner.current
    val cameraProviderFuture = remember { ProcessCameraProvider.getInstance(context) }
    val executor = remember { Executors.newSingleThreadExecutor() }

    DisposableEffect(Unit) {
        onDispose { executor.shutdown() }
    }

    key(analyzerMode) {
        AndroidView(
            modifier = modifier.fillMaxSize(),
            factory = { ctx ->
                val previewView = PreviewView(ctx).apply {
                    scaleType = PreviewView.ScaleType.FILL_CENTER
                }
                val preview = Preview.Builder().build().also {
                    it.setSurfaceProvider(previewView.surfaceProvider)
                }
                val analysis = ImageAnalysis.Builder()
                    .setTargetResolution(Size(1280, 720))
                    .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
                    .build()
                val analyzer = when (analyzerMode) {
                    AnalyzerMode.BARCODE -> BarcodeAnalyzer(onCodeDetected)
                    AnalyzerMode.OCR -> TextAnalyzer(onCodeDetected)
                }
                analysis.setAnalyzer(executor, analyzer)

                val selector = CameraSelector.DEFAULT_BACK_CAMERA
                cameraProviderFuture.addListener({
                    val provider = cameraProviderFuture.get()
                    provider.unbindAll()
                    provider.bindToLifecycle(
                        lifecycleOwner, selector, preview, analysis
                    )
                }, ContextCompat.getMainExecutor(context))

                previewView
            }
        )
    }

    DisposableEffect(Unit) {
        onDispose {
            if (cameraProviderFuture.isDone) {
                cameraProviderFuture.get().unbindAll()
            }
        }
    }
}
''',

    "app/src/main/java/com/example/componentfinder/camera/CameraScanActivity.kt": r'''package com.example.componentfinder.camera

import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import com.example.componentfinder.ui.theme.ComponentFinderTheme
import com.example.componentfinder.util.ModelExtractor
import com.google.mlkit.vision.barcode.BarcodeScanning
import com.google.mlkit.vision.common.InputImage
import com.google.mlkit.vision.text.TextRecognition
import com.google.mlkit.vision.text.latin.TextRecognizerOptions

class CameraScanActivity : ComponentActivity() {

    companion object {
        const val EXTRA_MODE = "mode"
        const val EXTRA_RESULT = "result"
        const val MODE_BARCODE = "barcode"
        const val MODE_OCR = "ocr"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val mode = intent.getStringExtra(EXTRA_MODE) ?: MODE_BARCODE

        setContent {
            ComponentFinderTheme {
                ScanScreen(mode = mode) { result ->
                    val data = Intent().apply {
                        putExtra(EXTRA_RESULT, result)
                        putExtra(EXTRA_MODE, mode)
                    }
                    setResult(RESULT_OK, data)
                    finish()
                }
            }
        }
    }
}

@Composable
fun ScanScreen(mode: String, onResult: (String) -> Unit) {
    val context = LocalContext.current
    val analyzerMode = if (mode == CameraScanActivity.MODE_OCR)
        AnalyzerMode.OCR else AnalyzerMode.BARCODE
    var rawText by remember { mutableStateOf<String?>(null) }
    var candidates by remember { mutableStateOf<List<String>>(emptyList()) }
    var editing by remember { mutableStateOf(false) }
    var editedText by remember { mutableStateOf("") }

    val imagePicker = rememberLauncherForActivityResult(
        ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        if (uri != null) {
            processLocalImage(context, uri, analyzerMode) { result ->
                if (result.isNotBlank()) {
                    rawText = result
                } else {
                    Toast.makeText(context, "未识别到内容", Toast.LENGTH_SHORT).show()
                }
            }
        }
    }

    LaunchedEffect(rawText) {
        rawText?.let {
            candidates = ModelExtractor.extractAll(it)
            editedText = candidates.firstOrNull() ?: it
        }
    }

    Box(modifier = Modifier.fillMaxSize()) {
        CameraPreview(
            analyzerMode = analyzerMode,
            onCodeDetected = { text ->
                if (rawText == null && text.isNotBlank()) {
                    rawText = text
                }
            }
        )

        Text(
            text = if (analyzerMode == AnalyzerMode.BARCODE)
                "对准条码/二维码" else "对准标签文字",
            modifier = Modifier
                .align(Alignment.TopCenter)
                .padding(top = 48.dp),
            color = MaterialTheme.colorScheme.onPrimary
        )

        Row(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.Center
        ) {
            Button(
                onClick = { imagePicker.launch("image/*") },
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.secondary
                )
            ) {
                Text("从相册选择图片")
            }
        }

        if (rawText != null) {
            Surface(
                modifier = Modifier
                    .align(Alignment.BottomCenter)
                    .fillMaxWidth()
                    .padding(bottom = 80.dp, start = 16.dp, end = 16.dp),
                tonalElevation = 6.dp
            ) {
                Column(
                    Modifier.padding(16.dp).verticalScroll(rememberScrollState())
                ) {
                    Text("原始识别：", style = MaterialTheme.typography.labelSmall)
                    Text(rawText!!, style = MaterialTheme.typography.bodySmall)
                    Spacer(Modifier.height(8.dp))

                    if (candidates.isNotEmpty()) {
                        Text("候选型号：", style = MaterialTheme.typography.labelSmall)
                        candidates.forEach { c ->
                            OutlinedButton(
                                onClick = { onResult(c) },
                                modifier = Modifier.fillMaxWidth().padding(vertical = 2.dp)
                            ) { Text(c) }
                        }
                    }

                    Spacer(Modifier.height(8.dp))

                    if (editing) {
                        OutlinedTextField(
                            value = editedText,
                            onValueChange = { editedText = it },
                            label = { Text("手动修正") },
                            modifier = Modifier.fillMaxWidth()
                        )
                        Spacer(Modifier.height(8.dp))
                        Button(
                            onClick = { onResult(editedText) },
                            modifier = Modifier.fillMaxWidth()
                        ) { Text("用修正后的查询") }
                    } else {
                        OutlinedButton(
                            onClick = { editing = true },
                            modifier = Modifier.fillMaxWidth()
                        ) { Text("手动修正") }
                    }

                    Spacer(Modifier.height(8.dp))
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceEvenly
                    ) {
                        OutlinedButton(onClick = {
                            rawText = null
                            candidates = emptyList()
                            editing = false
                        }) { Text("重扫") }
                    }
                }
            }
        }
    }
}

private fun processLocalImage(
    context: Context,
    uri: Uri,
    mode: AnalyzerMode,
    onResult: (String) -> Unit
) {
    val image = try {
        InputImage.fromFilePath(context, uri)
    } catch (e: Exception) {
        e.printStackTrace()
        onResult("")
        return
    }

    if (mode == AnalyzerMode.BARCODE) {
        val scanner = BarcodeScanning.getClient()
        scanner.process(image)
            .addOnSuccessListener { barcodes ->
                val result = barcodes.firstOrNull { it.rawValue != null }?.rawValue
                onResult(result ?: "")
            }
            .addOnFailureListener { onResult("") }
    } else {
        val recognizer = TextRecognition.getClient(TextRecognizerOptions.DEFAULT_OPTIONS)
        recognizer.process(image)
            .addOnSuccessListener { visionText ->
                onResult(visionText.text)
            }
            .addOnFailureListener { onResult("") }
    }
}
''',

    "app/src/main/java/com/example/componentfinder/bom/BomItem.kt": r'''package com.example.componentfinder.bom

import com.example.componentfinder.domain.model.ComponentSpec

data class BomItem(
    val lineNo: Int,
    val model: String,
    val qty: Int,
    val refDes: String = "",
    val spec: ComponentSpec? = null
)

data class BomSummary(
    val model: String,
    val totalQty: Int,
    val refDes: String,
    val spec: ComponentSpec?
)
''',

    "app/src/main/java/com/example/componentfinder/bom/BomParser.kt": r'''package com.example.componentfinder.bom

object BomParser {

    private val MODEL_KEYS = listOf("model", "p/n", "pn", "型号", "料号", "part", "mpn", "物料")
    private val QTY_KEYS = listOf("qty", "数量", "用量", "pcs", "count")
    private val REF_KEYS = listOf("ref", "位号", "designator", "location", "位置")

    fun parse(text: String): List<BomItem> {
        val lines = text.lines().map { it.trim() }.filter { it.isNotEmpty() }
        if (lines.isEmpty()) return emptyList()

        val first = lines.first().lowercase()
        val hasHeader = MODEL_KEYS.any { first.contains(it) } ||
                QTY_KEYS.any { first.contains(it) }

        val dataLines = if (hasHeader) lines.drop(1) else lines
        val delimiter = detectDelimiter(lines.firstOrNull() ?: "")

        var modelIdx = 0
        var qtyIdx = 1
        var refIdx = -1
        if (hasHeader) {
            val cols = splitLine(lines.first(), delimiter)
            modelIdx = -1; qtyIdx = -1; refIdx = -1
            cols.forEachIndexed { i, col ->
                val c = col.lowercase().trim()
                if (modelIdx < 0 && MODEL_KEYS.any { c.contains(it) }) modelIdx = i
                else if (qtyIdx < 0 && QTY_KEYS.any { c.contains(it) }) qtyIdx = i
                else if (refIdx < 0 && REF_KEYS.any { c.contains(it) }) refIdx = i
            }
            if (modelIdx < 0) modelIdx = 0
            if (qtyIdx < 0) qtyIdx = 1
        }

        val items = mutableListOf<BomItem>()
        dataLines.forEachIndexed { index, line ->
            val cols = splitLine(line, delimiter)
            if (cols.isEmpty()) return@forEachIndexed
            val model = cols.getOrNull(modelIdx)?.trim()?.trim('"') ?: return@forEachIndexed
            if (model.isBlank()) return@forEachIndexed
            val qty = cols.getOrNull(qtyIdx)?.trim()?.trim('"')?.toIntOrNull() ?: 1
            val ref = if (refIdx >= 0) cols.getOrNull(refIdx)?.trim()?.trim('"') ?: "" else ""
            items.add(
                BomItem(
                    lineNo = index + 1,
                    model = model,
                    qty = if (qty > 0) qty else 1,
                    refDes = ref
                )
            )
        }
        return items
    }

    private fun detectDelimiter(sample: String): Char {
        val candidates = listOf(',', '\t', ';', '|')
        return candidates.maxByOrNull { c -> sample.count { it == c } } ?: ','
    }

    private fun splitLine(line: String, delimiter: Char): List<String> {
        val result = mutableListOf<String>()
        val sb = StringBuilder()
        var inQuote = false
        for (ch in line) {
            when {
                ch == '"' -> inQuote = !inQuote
                ch == delimiter && !inQuote -> {
                    result.add(sb.toString()); sb.clear()
                }
                else -> sb.append(ch)
            }
        }
        result.add(sb.toString())
        return result
    }
}
''',

    "app/src/main/java/com/example/componentfinder/bom/BomRepository.kt": r'''package com.example.componentfinder.bom

import android.content.Context
import com.example.componentfinder.data.RulesRepository
import com.example.componentfinder.domain.parser.ParserEngine

class BomRepository(context: Context) {
    private val parser = ParserEngine(RulesRepository(context).loadRules())

    fun parseAll(items: List<BomItem>): List<BomItem> =
        items.map { it.copy(spec = parser.parse(it.model)) }

    fun summarize(items: List<BomItem>): List<BomSummary> {
        val map = LinkedHashMap<String, BomSummary>()
        items.forEach { item ->
            val existing = map[item.model]
            map[item.model] = if (existing == null) {
                BomSummary(item.model, item.qty, item.refDes, item.spec)
            } else {
                existing.copy(
                    totalQty = existing.totalQty + item.qty,
                    refDes = if (existing.refDes.isBlank()) item.refDes
                    else if (item.refDes.isBlank()) existing.refDes
                    else "${existing.refDes},${item.refDes}"
                )
            }
        }
        return map.values.toList()
    }
}
''',

    "app/src/main/java/com/example/componentfinder/bom/BomViewModel.kt": r'''package com.example.componentfinder.bom

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class BomViewModel(app: Application) : AndroidViewModel(app) {

    private val repo = BomRepository(app)

    private val _items = MutableStateFlow<List<BomItem>>(emptyList())
    val items: StateFlow<List<BomItem>> = _items

    private val _summary = MutableStateFlow<List<BomSummary>>(emptyList())
    val summary: StateFlow<List<BomSummary>> = _summary

    private val _loading = MutableStateFlow(false)
    val loading: StateFlow<Boolean> = _loading

    fun importText(text: String) {
        viewModelScope.launch {
            _loading.value = true
            val parsed = withContext(Dispatchers.Default) {
                val raw = BomParser.parse(text)
                repo.parseAll(raw)
            }
            _items.value = parsed
            _summary.value = repo.summarize(parsed)
            _loading.value = false
        }
    }

    fun clear() {
        _items.value = emptyList()
        _summary.value = emptyList()
    }
}
''',

    "app/src/main/java/com/example/componentfinder/bom/BomImportScreen.kt": r'''package com.example.componentfinder.bom

import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BomImportScreen(
    onBack: () -> Unit,
    onDone: () -> Unit,
    vm: BomViewModel = viewModel()
) {
    val context = LocalContext.current
    var textInput by remember { mutableStateOf("") }
    val loading by vm.loading.collectAsState()

    val fileLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.OpenDocument()
    ) { uri: Uri? ->
        if (uri != null) {
            val content = context.contentResolver
                .openInputStream(uri)?.bufferedReader()?.use { it.readText() } ?: ""
            textInput = content
            vm.importText(content)
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("导入 BOM") },
                navigationIcon = { IconButton(onClick = onBack) { Text("←") } }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .padding(padding)
                .padding(16.dp)
                .fillMaxSize()
                .verticalScroll(rememberScrollState()),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Text("支持 CSV / 文本粘贴", style = MaterialTheme.typography.bodySmall)

            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedButton(
                    onClick = {
                        fileLauncher.launch(arrayOf("text/*", "*/*"))
                    },
                    modifier = Modifier.weight(1f)
                ) { Text("选择文件") }

                OutlinedButton(
                    onClick = { vm.clear(); textInput = "" },
                    modifier = Modifier.weight(1f)
                ) { Text("清空") }
            }

            OutlinedTextField(
                value = textInput,
                onValueChange = { textInput = it },
                label = { Text("粘贴 BOM 内容") },
                minLines = 8,
                modifier = Modifier.fillMaxWidth()
            )

            Button(
                onClick = { vm.importText(textInput) },
                enabled = textInput.isNotBlank() && !loading,
                modifier = Modifier.fillMaxWidth()
            ) {
                if (loading) CircularProgressIndicator(
                    modifier = Modifier.size(18.dp), strokeWidth = 2.dp
                ) else Text("开始解析")
            }

            val items by vm.items.collectAsState()
            if (items.isNotEmpty()) {
                Text("已解析 ${items.size} 行", style = MaterialTheme.typography.bodyMedium)
                Button(onClick = onDone, modifier = Modifier.fillMaxWidth()) {
                    Text("查看结果")
                }
            }
        }
    }
}
''',

    "app/src/main/java/com/example/componentfinder/bom/BomResultScreen.kt": r'''package com.example.componentfinder.bom

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BomResultScreen(
    onBack: () -> Unit,
    vm: BomViewModel = viewModel()
) {
    val context = LocalContext.current
    val summary by vm.summary.collectAsState()
    var showSummary by remember { mutableStateOf(true) }
    val items by vm.items.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(if (showSummary) "汇总 (${summary.size})" else "明细 (${items.size})") },
                navigationIcon = { IconButton(onClick = onBack) { Text("←") } },
                actions = {
                    TextButton(onClick = { showSummary = !showSummary }) {
                        Text(if (showSummary) "明细" else "汇总")
                    }
                    TextButton(onClick = {
                        BomExporter.exportCsv(context, summary, items)
                    }) { Text("导出") }
                }
            )
        }
    ) { padding ->
        if (showSummary) {
            LazyColumn(
                modifier = Modifier.padding(padding).padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(summary) { s ->
                    BomCard(s.model, s.totalQty, s.refDes, s.spec)
                }
            }
        } else {
            LazyColumn(
                modifier = Modifier.padding(padding).padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(items) { item ->
                    BomCard("#${item.lineNo}  ${item.model}", item.qty, item.refDes, item.spec)
                }
            }
        }
    }
}

@Composable
private fun BomCard(
    title: String,
    qty: Int,
    refDes: String,
    spec: com.example.componentfinder.domain.model.ComponentSpec?
) {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(Modifier.padding(12.dp)) {
            Text(title, style = MaterialTheme.typography.titleSmall)
            Text("数量：$qty" + if (refDes.isNotBlank()) "  位号：$refDes" else "",
                style = MaterialTheme.typography.bodySmall)
            if (spec == null) {
                Text("⚠ 未识别该型号", color = MaterialTheme.colorScheme.error,
                    style = MaterialTheme.typography.bodySmall)
            } else {
                spec.toOrderedList().forEach { (k, v) ->
                    Text("$k：$v", style = MaterialTheme.typography.bodySmall)
                }
            }
        }
    }
}
''',

    "app/src/main/java/com/example/componentfinder/bom/BomExporter.kt": r'''package com.example.componentfinder.bom

import android.content.Context
import android.content.Intent
import androidx.core.content.FileProvider
import java.io.File

object BomExporter {

    fun exportCsv(
        context: Context,
        summary: List<BomSummary>,
        items: List<BomItem>
    ): String? {
        return try {
            val sb = StringBuilder()
            sb.append("型号,总数量,位号,封装,容值/阻值,精度,电压,材质,品牌\n")
            summary.forEach { s ->
                sb.append(
                    listOf(
                        s.model, s.totalQty.toString(), s.refDes,
                        s.spec?.packageName ?: "-", s.spec?.value ?: "-",
                        s.spec?.tolerance ?: "-", s.spec?.voltage ?: "-",
                        s.spec?.material ?: "-", s.spec?.brand ?: "-"
                    ).joinToString(",") { it.replace(",", " ") }
                ).append("\n")
            }
            sb.append("\n明细\n")
            sb.append("行号,型号,数量,位号,封装,容值/阻值,精度,电压,材质,品牌\n")
            items.forEach { i ->
                sb.append(
                    listOf(
                        i.lineNo.toString(), i.model, i.qty.toString(), i.refDes,
                        i.spec?.packageName ?: "-", i.spec?.value ?: "-",
                        i.spec?.tolerance ?: "-", i.spec?.voltage ?: "-",
                        i.spec?.material ?: "-", i.spec?.brand ?: "-"
                    ).joinToString(",") { it.replace(",", " ") }
                ).append("\n")
            }

            val file = File(context.cacheDir, "bom_export.csv")
            file.writeText(sb.toString(), Charsets.UTF_8)

            val uri = FileProvider.getUriForFile(
                context, "${context.packageName}.fileprovider", file
            )
            val intent = Intent(Intent.ACTION_SEND).apply {
                type = "text/csv"
                putExtra(Intent.EXTRA_STREAM, uri)
                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            context.startActivity(Intent.createChooser(intent, "导出 BOM"))
            null
        } catch (e: Exception) {
            "导出失败：${e.message}"
        }
    }
}
''',

    "app/src/main/java/com/example/componentfinder/ui/theme/Theme.kt": r'''package com.example.componentfinder.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable

@Composable
fun ComponentFinderTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colors = if (darkTheme) darkColorScheme() else lightColorScheme()
    MaterialTheme(colorScheme = colors, content = content)
}
''',

    "app/src/main/java/com/example/componentfinder/ui/navigation/AppNav.kt": r'''package com.example.componentfinder.ui.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.componentfinder.bom.BomImportScreen
import com.example.componentfinder.bom.BomResultScreen
import com.example.componentfinder.ui.converter.UnitConverterScreen
import com.example.componentfinder.ui.history.HistoryScreen
import com.example.componentfinder.ui.home.HomeScreen
import com.example.componentfinder.ui.result.ResultScreen

@Composable
fun AppNav(startDestination: String = "home") {
    val nav = rememberNavController()
    NavHost(navController = nav, startDestination = startDestination) {

        composable("home") {
            HomeScreen(
                onResult = { model ->
                    val encoded = java.net.URLEncoder.encode(model, "UTF-8")
                    nav.navigate("result/$encoded")
                },
                onBomImport = { nav.navigate("bom_import") },
                onHistory = { nav.navigate("history") },
                onConverter = { nav.navigate("converter") }
            )
        }
        composable("result/{model}") { entry ->
            val model = java.net.URLDecoder.decode(
                entry.arguments?.getString("model") ?: "", "UTF-8"
            )
            ResultScreen(model = model, onBack = { nav.popBackStack() })
        }
        composable("history") {
            HistoryScreen(onBack = { nav.popBackStack() })
        }
        composable("converter") {
            UnitConverterScreen(onBack = { nav.popBackStack() })
        }
        composable("bom_import") {
            BomImportScreen(
                onBack = { nav.popBackStack() },
                onDone = { nav.navigate("bom_result") }
            )
        }
        composable("bom_result") {
            BomResultScreen(onBack = { nav.popBackStack() })
        }
    }
}
''',

    "app/src/main/java/com/example/componentfinder/ui/home/HomeScreen.kt": r'''package com.example.componentfinder.ui.home

import android.app.Activity
import android.content.Intent
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import com.example.componentfinder.camera.CameraScanActivity
import com.example.componentfinder.util.rememberCameraPermissionState

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    onResult: (String) -> Unit,
    onBomImport: () -> Unit = {},
    onHistory: () -> Unit = {},
    onConverter: () -> Unit = {}
) {
    val context = LocalContext.current
    var input by remember { mutableStateOf("") }
    val (hasPermission, requestPermission) = rememberCameraPermissionState()

    val scanLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == Activity.RESULT_OK) {
            val text = result.data?.getStringExtra(CameraScanActivity.EXTRA_RESULT)
            if (!text.isNullOrBlank()) {
                onResult(text)
            }
        }
    }

    fun launchScan(mode: String) {
        if (!hasPermission) { requestPermission(); return }
        val intent = Intent(context, CameraScanActivity::class.java).apply {
            putExtra(CameraScanActivity.EXTRA_MODE, mode)
        }
        scanLauncher.launch(intent)
    }

    Scaffold(topBar = { TopAppBar(title = { Text("元件快查 v1.3") }) }) { padding ->
        Column(
            modifier = Modifier
                .padding(padding).padding(16.dp).fillMaxSize(),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            OutlinedTextField(
                value = input,
                onValueChange = { input = it },
                label = { Text("输入型号 / 丝印（如 104、1001、01B）") },
                modifier = Modifier.fillMaxWidth()
            )
            Button(
                onClick = { if (input.isNotBlank()) onResult(input) },
                modifier = Modifier.fillMaxWidth()
            ) { Text("查询") }

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                OutlinedButton(
                    onClick = { launchScan(CameraScanActivity.MODE_BARCODE) },
                    modifier = Modifier.weight(1f)
                ) { Text("扫码") }
                OutlinedButton(
                    onClick = { launchScan(CameraScanActivity.MODE_OCR) },
                    modifier = Modifier.weight(1f)
                ) { Text("拍照识别") }
            }

            HorizontalDivider()

            OutlinedButton(
                onClick = onBomImport,
                modifier = Modifier.fillMaxWidth()
            ) { Text("导入 BOM") }

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                OutlinedButton(onClick = onHistory, modifier = Modifier.weight(1f)) { Text("历史记录") }
                OutlinedButton(onClick = onConverter, modifier = Modifier.weight(1f)) { Text("单位换算") }
            }

            Card(modifier = Modifier.fillMaxWidth()) {
                Column(Modifier.padding(12.dp)) {
                    Text("💡 丝印查询示例", style = MaterialTheme.typography.titleSmall)
                    Text("• 104 → 电容 100nF / 电阻 100kΩ", style = MaterialTheme.typography.bodySmall)
                    Text("• 1001 → 电阻 1kΩ (±1%)", style = MaterialTheme.typography.bodySmall)
                    Text("• 01B → 电阻 1kΩ (±1%, 0603)", style = MaterialTheme.typography.bodySmall)
                }
            }
            Text("版本 v1.3", style = MaterialTheme.typography.labelSmall)
        }
    }
}
''',

    "app/src/main/java/com/example/componentfinder/ui/result/ResultScreen.kt": r'''package com.example.componentfinder.ui.result

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import com.example.componentfinder.data.HistoryRepository
import com.example.componentfinder.data.RulesRepository
import com.example.componentfinder.domain.parser.ParserEngine

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ResultScreen(model: String, onBack: () -> Unit) {
    val context = LocalContext.current
    val rules = remember { RulesRepository(context).loadRules() }
    val parser = remember { ParserEngine(rules) }
    val specs = remember(model) { parser.parseAll(model) }
    val historyRepo = remember { HistoryRepository(context) }

    LaunchedEffect(specs) {
        specs.firstOrNull()?.let { historyRepo.save(model, it) }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("解析结果") },
                navigationIcon = { IconButton(onClick = onBack) { Text("←") } }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .padding(padding).padding(16.dp).fillMaxSize()
                .verticalScroll(rememberScrollState()),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Text("原始输入：$model", style = MaterialTheme.typography.bodySmall)
            HorizontalDivider()

            if (specs.isEmpty()) {
                Card(
                    colors = CardDefaults.cardColors(
                        containerColor = MaterialTheme.colorScheme.errorContainer
                    ),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(Modifier.padding(12.dp)) {
                        Text("未识别", style = MaterialTheme.typography.titleMedium)
                        Spacer(Modifier.height(4.dp))
                        Text("请检查输入或补充规则库", style = MaterialTheme.typography.bodySmall)
                    }
                }
            } else {
                Text(
                    "共找到 ${specs.size} 个可能结果：",
                    style = MaterialTheme.typography.titleSmall,
                    color = MaterialTheme.colorScheme.primary
                )
                specs.forEachIndexed { idx, spec ->
                    Card(modifier = Modifier.fillMaxWidth()) {
                        Column(Modifier.padding(12.dp)) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween
                            ) {
                                Text(
                                    "【${spec.type}】${if (specs.size > 1) "候选${idx + 1}" else ""}",
                                    style = MaterialTheme.typography.titleMedium,
                                    color = MaterialTheme.colorScheme.primary
                                )
                            }
                            Spacer(Modifier.height(8.dp))
                            spec.toOrderedList().forEach { (k, v) ->
                                if (v != "-" && v.isNotEmpty()) {
                                    Row(
                                        modifier = Modifier.fillMaxWidth().padding(vertical = 2.dp),
                                        horizontalArrangement = Arrangement.SpaceBetween
                                    ) {
                                        Text(k, style = MaterialTheme.typography.bodyMedium)
                                        Text(v, style = MaterialTheme.typography.bodyMedium)
                                    }
                                }
                            }
                            Spacer(Modifier.height(8.dp))
                            Text(
                                getExplanation(spec.type),
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }
            }
        }
    }
}

private fun getExplanation(type: String): String {
    return when (type) {
        "电阻" -> """
            |注：
            |• 贴片电阻常见 E24 系列和 E96 系列。
            |• E24 精度为 ±5%，E96 系列精度 ±1%。
            |• E24 采用三位数值表示，如 102、222、473。
            |• E96 采用四位数值表示，如 1001、4702；或代码表示，如 01B、22B。
        """.trimMargin()
        "电容" -> """
            |注：
            |• 精度等级：J(±5%)、K(±10%)、M(±20%)。
            |• 材质：NPO/C0G 高稳定，X7R 中等，X5R 一般，Y5V 低。
            |• 换算：1µF = 1000nF = 1,000,000pF。
        """.trimMargin()
        else -> ""
    }
}
''',

    "app/src/main/java/com/example/componentfinder/ui/history/HistoryScreen.kt": r'''package com.example.componentfinder.ui.history

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import com.example.componentfinder.data.HistoryRepository

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HistoryScreen(onBack: () -> Unit) {
    val context = LocalContext.current
    val repo = remember { HistoryRepository(context) }
    val list by repo.getAll().collectAsState(initial = emptyList())

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("历史记录") },
                navigationIcon = { IconButton(onClick = onBack) { Text("←") } }
            )
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier.padding(padding).padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(list) { item ->
                Card(modifier = Modifier.fillMaxWidth()) {
                    Column(Modifier.padding(12.dp)) {
                        Text(item.model, style = MaterialTheme.typography.titleSmall)
                        Text("封装：${item.packageName}  容值/阻值：${item.value}", style = MaterialTheme.typography.bodySmall)
                        Text("精度：${item.tolerance}  电压：${item.voltage}", style = MaterialTheme.typography.bodySmall)
                        Text("材质：${item.material}  品牌：${item.brand}", style = MaterialTheme.typography.bodySmall)
                    }
                }
            }
        }
    }
}
''',

    "app/src/main/java/com/example/componentfinder/ui/converter/UnitConverterScreen.kt": r'''package com.example.componentfinder.ui.converter

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.example.componentfinder.domain.parser.SMDCodeParser

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun UnitConverterScreen(onBack: () -> Unit) {
    var input by remember { mutableStateOf("") }
    var result by remember { mutableStateOf("") }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("单位换算 / 丝印查询") },
                navigationIcon = { IconButton(onClick = onBack) { Text("←") } }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier.padding(padding).padding(16.dp).fillMaxSize()
                .verticalScroll(rememberScrollState()),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            OutlinedTextField(
                value = input,
                onValueChange = { input = it },
                label = { Text("输入丝印(104) 或 数值(100nF / 10kΩ)") },
                modifier = Modifier.fillMaxWidth()
            )
            Button(
                onClick = { result = convertSmart(input) },
                modifier = Modifier.fillMaxWidth()
            ) { Text("换算") }

            if (result.isNotEmpty()) {
                Card(modifier = Modifier.fillMaxWidth()) {
                    Text(
                        result,
                        modifier = Modifier.padding(16.dp),
                        style = MaterialTheme.typography.bodyLarge
                    )
                }
            }

            Card(modifier = Modifier.fillMaxWidth()) {
                Column(Modifier.padding(12.dp)) {
                    Text("💡 示例", style = MaterialTheme.typography.titleSmall)
                    Text("• 104 → 电容 100nF / 电阻 100kΩ", style = MaterialTheme.typography.bodySmall)
                    Text("• 1001 → 电阻 1kΩ (E96, ±1%)", style = MaterialTheme.typography.bodySmall)
                    Text("• 01B → 电阻 1kΩ (E96 代码, 0603)", style = MaterialTheme.typography.bodySmall)
                    Text("• 100nF → 100000 pF / 0.1 µF", style = MaterialTheme.typography.bodySmall)
                    Text("• 10kΩ → 10000 Ω / 0.01 MΩ", style = MaterialTheme.typography.bodySmall)
                }
            }
        }
    }
}

private fun convertSmart(input: String): String {
    val s = input.trim().replace(" ", "").uppercase()
    if (s.isEmpty()) return "请输入内容"

    val isSMDCode = s.matches(Regex("^\\d{3,4}$")) ||
            s.matches(Regex("^\\d{2}[A-Z]$")) ||
            s.matches(Regex("^\\d+[Rr]\\d+$"))

    if (isSMDCode) {
        val specs = SMDCodeParser.parseAll(s)
        if (specs.isNotEmpty()) {
            val sb = StringBuilder()
            sb.append("「").append(input).append("」识别为丝印代码：\n\n")
            specs.forEach { spec ->
                sb.append("【").append(spec.type).append("】\n")
                spec.toOrderedList().forEach { (k, v) ->
                    if (v != "-" && v.isNotEmpty()) sb.append("  ").append(k).append("：").append(v).append("\n")
                }
                sb.append("\n")
            }
            sb.append("注：\n")
            sb.append("• 电阻 E24(3位)±5%，E96(4位或代码)±1%\n")
            sb.append("• 电容 104=100nF 等")
            return sb.toString().trim()
        }
    }

    val capRegex = Regex("([\\d.]+)\\s*(pf|nf|uf|µf|f)", RegexOption.IGNORE_CASE)
    val resRegex = Regex("([\\d.]+)\\s*(m?[ωΩ]|m?ohm|k|K|M|r|R)", RegexOption.IGNORE_CASE)

    if (capRegex.containsMatchIn(s)) return convertCap(input)
    if (resRegex.containsMatchIn(s) || s.contains("欧")) return convertRes(input)

    return "无法识别格式。\n示例：\n• 丝印 104 / 1001 / 01B\n• 数值 100nF / 10kΩ / 4R7"
}

private fun fmt(v: Double): String {
    val r = Math.round(v * 1_000_000.0) / 1_000_000.0
    return if (r == r.toLong().toDouble()) r.toLong().toString() else r.toString()
}

private fun convertCap(input: String): String {
    val m = Regex("([\\d.]+)\\s*(pf|nf|uf|µf|f)", RegexOption.IGNORE_CASE).find(input)
        ?: return "格式错误，示例：100nF、1uF、0.1uf"
    val v = m.groupValues[1].toDouble()
    val unit = m.groupValues[2].lowercase().replace("µ", "u")
    val pfValue = when (unit) {
        "pf" -> v
        "nf" -> v * 1000
        "uf" -> v * 1_000_000
        "f" -> v * 1_000_000_000_000
        else -> return "未知单位"
    }
    return "输入：$input\n" +
            "= ${fmt(pfValue)} pF\n" +
            "= ${fmt(pfValue / 1000)} nF\n" +
            "= ${fmt(pfValue / 1_000_000)} µF\n" +
            "= ${fmt(pfValue / 1_000_000_000_000)} F"
}

private fun convertRes(input: String): String {
    val s = input.trim().replace(" ", "").replace("欧", "")
    val m = Regex("([\\d.]+)(m?[ωΩ]|m?ohm|[kK]|[Mm]|[rR])?", RegexOption.IGNORE_CASE).find(s)
        ?: return "格式错误，示例：10kΩ、1M、4R7"
    val v = m.groupValues[1].toDoubleOrNull() ?: return "数值格式错误"
    val rawUnit = m.groupValues[2]
    val ohmValue = when (rawUnit.lowercase()) {
        "mω", "mohm" -> v / 1000
        "k", "kω", "kohm" -> v * 1000
        "m" -> v * 1_000_000
        "r" -> v
        else -> v
    }
    return "输入：$input\n" +
            "= ${fmt(ohmValue)} Ω\n" +
            "= ${fmt(ohmValue / 1000)} kΩ\n" +
            "= ${fmt(ohmValue / 1_000_000)} MΩ"
}
''',

    "app/src/main/java/com/example/componentfinder/widget/ScanWidgetProvider.kt": r'''package com.example.componentfinder.widget

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.Context
import android.content.Intent
import android.widget.RemoteViews
import com.example.componentfinder.R
import com.example.componentfinder.camera.CameraScanActivity

class ScanWidgetProvider : AppWidgetProvider() {
    override fun onUpdate(
        context: Context,
        appWidgetManager: AppWidgetManager,
        appWidgetIds: IntArray
    ) {
        for (id in appWidgetIds) {
            val intent = Intent(context, CameraScanActivity::class.java).apply {
                putExtra(CameraScanActivity.EXTRA_MODE, CameraScanActivity.MODE_BARCODE)
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            val pending = PendingIntent.getActivity(
                context, 1001, intent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            val views = RemoteViews(context.packageName, R.layout.widget_scan).apply {
                setOnClickPendingIntent(R.id.widget_root, pending)
            }
            appWidgetManager.updateAppWidget(id, views)
        }
    }
}
''',

    "app/src/main/java/com/example/componentfinder/widget/OcrWidgetProvider.kt": r'''package com.example.componentfinder.widget

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.Context
import android.content.Intent
import android.widget.RemoteViews
import com.example.componentfinder.R
import com.example.componentfinder.camera.CameraScanActivity

class OcrWidgetProvider : AppWidgetProvider() {
    override fun onUpdate(
        context: Context,
        appWidgetManager: AppWidgetManager,
        appWidgetIds: IntArray
    ) {
        for (id in appWidgetIds) {
            val intent = Intent(context, CameraScanActivity::class.java).apply {
                putExtra(CameraScanActivity.EXTRA_MODE, CameraScanActivity.MODE_OCR)
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            val pending = PendingIntent.getActivity(
                context, 1002, intent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            val views = RemoteViews(context.packageName, R.layout.widget_ocr).apply {
                setOnClickPendingIntent(R.id.widget_root, pending)
            }
            appWidgetManager.updateAppWidget(id, views)
        }
    }
}
''',

    "app/src/main/java/com/example/componentfinder/widget/ConverterWidgetProvider.kt": r'''package com.example.componentfinder.widget

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.Context
import android.content.Intent
import android.widget.RemoteViews
import com.example.componentfinder.MainActivity
import com.example.componentfinder.R

class ConverterWidgetProvider : AppWidgetProvider() {
    override fun onUpdate(
        context: Context,
        appWidgetManager: AppWidgetManager,
        appWidgetIds: IntArray
    ) {
        for (id in appWidgetIds) {
            val intent = Intent(context, MainActivity::class.java).apply {
                putExtra("open_converter", true)
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            val pending = PendingIntent.getActivity(
                context, 1003, intent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            val views = RemoteViews(context.packageName, R.layout.widget_converter).apply {
                setOnClickPendingIntent(R.id.widget_root, pending)
            }
            appWidgetManager.updateAppWidget(id, views)
        }
    }
}
''',
}

for path, content in files.items():
    full = os.path.join(base, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

print("项目生成完成，请用 Android Studio 打开：" + base)
print("下一步：压缩 ComponentFinder 文件夹为 ComponentFinder.zip，上传到 GitHub")