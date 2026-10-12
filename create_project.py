import os

base = "ComponentFinder"

files = {
    "settings.gradle.kts": r'''pluginManagement {
    repositories { google(); mavenCentral(); gradlePluginPortal() }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories { google(); mavenCentral() }
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
        versionCode = 20
        versionName = "2.0"
    }

    splits {
        abi {
            isEnable = true
            reset()
            include("arm64-v8a")
            isUniversalApk = false
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
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

    "app/proguard-rules.pro": r'''# 空
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
        <activity android:name=".MainActivity" android:exported="true" android:excludeFromRecents="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        <activity android:name=".camera.CameraScanActivity"
            android:screenOrientation="portrait" android:excludeFromRecents="true"
            android:theme="@style/Theme.ComponentFinder" />
        <provider android:name="androidx.core.content.FileProvider"
            android:authorities="${applicationId}.fileprovider"
            android:exported="false" android:grantUriPermissions="true">
            <meta-data android:name="android.support.FILE_PROVIDER_PATHS"
                android:resource="@xml/file_paths" />
        </provider>
    </application>
</manifest>
''',

    "app/src/main/res/values/strings.xml": r'''<resources><string name="app_name">元件快查</string></resources>
''',

    "app/src/main/res/values/themes.xml": r'''<resources>
    <style name="Theme.ComponentFinder" parent="android:Theme.Material.Light.NoActionBar" />
</resources>
''',

    "app/src/main/res/xml/file_paths.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<paths><cache-path name="cache" path="." /></paths>
''',

    "app/src/main/assets/rules.json": r'''[
  {
    "brand": "YAGEO", "type": "电容",
    "pattern": "^CC(0603|0805|1206)([A-Z]{2})(NPO|X7R|X5R)([0-9A-Z]{3})(\\d{3})$",
    "packageGroup": 1, "toleranceGroup": 2, "materialGroup": 3, "voltageGroup": 4, "valueGroup": 5
  },
  {
    "brand": "YAGEO", "type": "电阻",
    "pattern": "^RC(0603|0805|1206)([A-Z]{2})-?(\\d{2})([0-9A-Z]{3,4})$",
    "packageGroup": 1, "toleranceGroup": 2, "valueGroup": 4, "voltageGroup": -1, "materialGroup": -1
  },
  {
    "brand": "SAMSUNG", "type": "电容",
    "pattern": "^CL(03|05|10|21|31|43)([A-Z])(\\d{3})([A-Z])([0-9A-Z])(\\d)([A-Z]{3})$",
    "packageGroup": 1, "materialGroup": 2, "valueGroup": 3, "toleranceGroup": 4, "voltageGroup": 5
  },
  {
    "brand": "CCTC", "type": "电容",
    "pattern": "^TCC(0603|0805|1206)(X7R|X5R|NPO|C0G)(\\d{3})([A-Z])(\\d{3})([A-Z]{2})$",
    "packageGroup": 1, "materialGroup": 2, "valueGroup": 3, "toleranceGroup": 4, "voltageGroup": 5
  },
  {
    "brand": "FH", "type": "电容",
    "pattern": "^(0603|0805|1206)([A-Z]{1,2})(\\d{3})([A-Z])(\\d{3})(NT)$",
    "packageGroup": 1, "materialGroup": 2, "valueGroup": 3, "toleranceGroup": 4, "voltageGroup": 5
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
        setContent {
            ComponentFinderTheme { AppNav() }
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
                type = "电容", packageName = "未知",
                value = formatCapacitance(pf),
                tolerance = "常见 ±5% (J) / ±10% (K) / ±20% (M)",
                voltage = "需结合封装", quantity = "-",
                material = "需结合完整型号", brand = "通用丝印"
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
                type = "电阻", packageName = "未知",
                value = formatResistance(ohm),
                tolerance = "±1% (E96系列)", voltage = "-", quantity = "-",
                material = "厚膜", brand = "E96 数值表示"
            )
        }
        Regex("^(\\d{3})$").find(code)?.let { m ->
            val value = m.groupValues[1]
            val base = value.substring(0, 2).toDouble()
            val mult = value.substring(2).toInt()
            val ohm = base * Math.pow(10.0, mult.toDouble())
            return ComponentSpec(
                type = "电阻", packageName = "未知",
                value = formatResistance(ohm),
                tolerance = "±5% (E24系列)", voltage = "-", quantity = "-",
                material = "厚膜", brand = "E24 数值表示"
            )
        }
        Regex("^(\\d{2})([A-Z])$").find(code)?.let { m ->
            val baseCode = m.groupValues[1]
            val multCode = m.groupValues[2]
            val baseValue = E96_BASE_VALUES[baseCode] ?: return null
            val mult = E96_MULTIPLIERS[multCode] ?: return null
            val ohm = baseValue * Math.pow(10.0, mult.toDouble())
            return ComponentSpec(
                type = "电阻", packageName = "常见0603",
                value = formatResistance(ohm),
                tolerance = "±1% (E96系列)", voltage = "-", quantity = "-",
                material = "厚膜", brand = "E96 代码表示"
            )
        }
        return null
    }

    private fun formatCapacitance(pf: Double): String = when {
        pf >= 1_000_000 -> "${formatNumber(pf / 1_000_000)} µF"
        pf >= 1000 -> "${formatNumber(pf / 1000)} nF"
        else -> "${formatNumber(pf)} pF"
    }

    private fun formatResistance(ohm: Double): String = when {
        ohm >= 1_000_000 -> "${formatNumber(ohm / 1_000_000)} MΩ"
        ohm >= 1000 -> "${formatNumber(ohm / 1000)} kΩ"
        else -> "${formatNumber(ohm)} Ω"
    }

    private fun formatNumber(num: Double): String {
        val r = Math.round(num * 1000.0) / 1000.0
        return if (r == r.toLong().toDouble()) r.toLong().toString() else r.toString()
    }
}
''',

    "app/src/main/java/com/example/componentfinder/domain/parser/ParserEngine.kt": r'''package com.example.componentfinder.domain.parser

import com.example.componentfinder.domain.model.ComponentSpec
import com.example.componentfinder.domain.model.Rule

class ParserEngine(private val rules: List<Rule>) {

    fun parseAll(input: String): List<ComponentSpec> {
        val clean = input.trim().uppercase().replace(" ", "").replace("\n", "").replace("\t", "")
        val results = LinkedHashSet<ComponentSpec>()

        for (rule in rules) {
            rule.pattern.matchEntire(clean)?.let { results.add(buildSpec(rule, it)) }
        }
        if (results.isNotEmpty()) return results.toList()

        for (candidate in extractCandidates(clean)) {
            for (rule in rules) {
                rule.pattern.matchEntire(candidate)?.let { results.add(buildSpec(rule, it)) }
            }
        }
        if (results.isNotEmpty()) return results.toList()

        SMDCodeParser.parseAll(clean).forEach { results.add(it) }
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
        return result
    }
}
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
        return c
    }
    private fun formatCap(pf: Double): String = when {
        pf >= 1_000_000 -> "${trim(pf / 1_000_000)} µF"
        pf >= 1000 -> "${trim(pf / 1000)} nF"
        else -> "${trim(pf)} pF"
    }
    fun resValue(code: String): String {
        val c = code.uppercase().replace(" ", "")
        if (c.matches(Regex("\\d{3,4}"))) {
            val digits = c.length
            val base = if (digits == 3) c.substring(0, 2).toInt() else c.substring(0, 3).toInt()
            val mult = c.last().toString().toInt()
            return formatRes(base * Math.pow(10.0, mult.toDouble()))
        }
        return c
    }
    private fun formatRes(ohm: Double): String = when {
        ohm >= 1_000_000 -> "${trim(ohm / 1_000_000)} MΩ"
        ohm >= 1000 -> "${trim(ohm / 1000)} kΩ"
        else -> "${trim(ohm)} Ω"
    }
    fun voltage(code: String): String = when (code.uppercase()) {
        "9BN","9BB","B8","500","1H" -> "50V"
        "0BN","OBN","0BB","OBB","8BB","1E" -> "25V"
        "7BB","1C" -> "16V"
        "5BB","0J" -> "6.3V"
        "C8","101","2A" -> "100V"
        "2E","251" -> "250V"
        "102","1K" -> "1000V"
        "451" -> "450V"
        "160" -> "16V"
        else -> "-"
    }
    fun material(code: String): String {
        val c = code.uppercase()
        return when {
            c.contains("NPO")||c.contains("C0G")||c.contains("CG") -> "NPO (C0G)"
            c.contains("X7R") -> "X7R"
            c.contains("X5R") -> "X5R"
            c.contains("Y5V") -> "Y5V"
            else -> "-"
        }
    }
    fun tolerance(code: String): String {
        val c = code.uppercase()
        val key = if (c.isNotEmpty() && c[0] in "JKMFGBCDZ") c[0].toString() else c
        return when (key) {
            "J" -> "±5%"; "K" -> "±10%"; "M" -> "±20%"
            "F" -> "±1%"; "G" -> "±2%"; "B" -> "±0.1%"
            "C" -> "±0.25%"; "D" -> "±0.5%"
            else -> "-"
        }
    }
    private fun trim(v: Double): String {
        val r = Math.round(v * 1000.0) / 1000.0
        return if (r == r.toLong().toDouble()) r.toLong().toString() else r.toString()
    }
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
            rules.add(Rule(
                brand = obj.getString("brand"),
                type = obj.getString("type"),
                pattern = Regex(obj.getString("pattern")),
                packageGroup = obj.optInt("packageGroup", -1),
                valueGroup = obj.optInt("valueGroup", -1),
                toleranceGroup = obj.optInt("toleranceGroup", -1),
                voltageGroup = obj.optInt("voltageGroup", -1),
                materialGroup = obj.optInt("materialGroup", -1)
            ))
        }
        return rules
    }
}
''',

    "app/src/main/java/com/example/componentfinder/ui/theme/Theme.kt": r'''package com.example.componentfinder.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable

@Composable
fun ComponentFinderTheme(content: @Composable () -> Unit) {
    MaterialTheme(colorScheme = lightColorScheme(), content = content)
}
''',

    "app/src/main/java/com/example/componentfinder/ui/navigation/AppNav.kt": r'''package com.example.componentfinder.ui.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.componentfinder.ui.home.HomeScreen
import com.example.componentfinder.ui.result.ResultScreen

@Composable
fun AppNav() {
    val nav = rememberNavController()
    NavHost(navController = nav, startDestination = "home") {
        composable("home") {
            HomeScreen(onResult = { model ->
                val encoded = java.net.URLEncoder.encode(model, "UTF-8")
                nav.navigate("result/$encoded")
            })
        }
        composable("result/{model}") { entry ->
            val model = java.net.URLDecoder.decode(
                entry.arguments?.getString("model") ?: "", "UTF-8"
            )
            ResultScreen(model = model, onBack = { nav.popBackStack() })
        }
    }
}
''',

    "app/src/main/java/com/example/componentfinder/ui/home/HomeScreen.kt": r'''package com.example.componentfinder.ui.home

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(onResult: (String) -> Unit) {
    var input by remember { mutableStateOf("") }

    Scaffold(topBar = { TopAppBar(title = { Text("元件快查 v2.0") }) }) { padding ->
        Column(
            modifier = Modifier.padding(padding).padding(16.dp).fillMaxSize()
                .verticalScroll(rememberScrollState()),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            // 醒目的版本号横幅
            Card(
                colors = CardDefaults.cardColors(containerColor = Color(0xFF1976D2)),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(Modifier.padding(12.dp)) {
                    Text("🎉 版本 v2.0", color = Color.White,
                        style = MaterialTheme.typography.titleMedium)
                    Text("如果你看到这行字，说明装的是最新版",
                        color = Color.White, style = MaterialTheme.typography.bodySmall)
                }
            }

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

            // 一键测试
            Button(
                onClick = { onResult("104") },
                modifier = Modifier.fillMaxWidth(),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF4CAF50))
            ) { Text("🧪 一键测试：查询 104") }

            Card(modifier = Modifier.fillMaxWidth()) {
                Column(Modifier.padding(12.dp)) {
                    Text("💡 应该看到什么？", style = MaterialTheme.typography.titleSmall)
                    Text("• 104 → 电容 100nF + 电阻 100kΩ", style = MaterialTheme.typography.bodySmall)
                    Text("• 1001 → 电阻 1kΩ (±1%)", style = MaterialTheme.typography.bodySmall)
                    Text("• 01B → 电阻 1kΩ (±1%, 0603)", style = MaterialTheme.typography.bodySmall)
                }
            }
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
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import com.example.componentfinder.data.RulesRepository
import com.example.componentfinder.domain.parser.ParserEngine

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ResultScreen(model: String, onBack: () -> Unit) {
    val context = LocalContext.current
    val rules = remember { RulesRepository(context).loadRules() }
    val parser = remember { ParserEngine(rules) }
    val specs = remember(model) { parser.parseAll(model) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("解析结果") },
                navigationIcon = { IconButton(onClick = onBack) { Text("←") } }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier.padding(padding).padding(16.dp).fillMaxSize()
                .verticalScroll(rememberScrollState()),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Text("原始输入：$model", style = MaterialTheme.typography.bodySmall)
            HorizontalDivider()

            if (specs.isEmpty()) {
                Card(
                    colors = CardDefaults.cardColors(containerColor = Color(0xFFFFCDD2)),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(Modifier.padding(16.dp)) {
                        Text("❌ 未识别", style = MaterialTheme.typography.titleMedium)
                        Text("版本 v2.0 - 如果你看到这行，说明代码是最新的",
                            style = MaterialTheme.typography.bodySmall)
                    }
                }
            } else {
                Text("共找到 ${specs.size} 个结果：",
                    style = MaterialTheme.typography.titleSmall,
                    color = MaterialTheme.colorScheme.primary)
                specs.forEachIndexed { idx, spec ->
                    Card(modifier = Modifier.fillMaxWidth()) {
                        Column(Modifier.padding(12.dp)) {
                            Text("【${spec.type}】候选 ${idx + 1}",
                                style = MaterialTheme.typography.titleMedium,
                                color = MaterialTheme.colorScheme.primary)
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
                        }
                    }
                }
            }
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

print("项目生成完成：" + base)
print("请压缩 ComponentFinder 为 ComponentFinder.zip，删除 GitHub 上的旧 zip 后上传")