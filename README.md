# أداة اختبار الحمل - Load Testing App

<div dir="rtl">

## 🚀 نظرة عامة

تطبيق سطح مكتب Python مع واجهة رسومية عربية (RTL) لاختبار حمل المواقع باستخدام ApacheBench.

## ✨ الميزات

- 🌐 واجهة مستخدم عربية كاملة مع دعم RTL
- 📊 إدخال URL وعدد الطلبات والطلبات المتزامنة
- 🔄 خيار Keep-Alive
- 📈 عرض النتائج الخام والملخص
- 📋 نسخ وتصدير النتائج (JSON/TXT)
- ⏹️ إيقاف الاختبار أثناء التنفيذ

## 📦 متطلبات التثبيت

```bash
pip install PySide6>=6.5.0
```

## 🏃 تشغيل التطبيق

### Windows
```batch
run.bat
```

أو:
```bash
python src/main.py
```

## 📁 هيكل المشروع

```
testHTTPrequest/
├── src/
│   ├── main.py              # نقطة الدخول
│   ├── arabic_ui.py         # النصوص العربية
│   ├── ab_runner.py         # تشغيل ApacheBench
│   ├── ab_resolver.py       # تحديد مسار ab.exe
│   ├── parser.py            # تحليل النتائج
│   ├── exporter.py          # تصدير النتائج
│   └── ui/
│       ├── main_window.py   # النافذة الرئيسية
│       ├── input_panel.py   # لوحة الإدخال
│       ├── results_panel.py # لوحة النتائج
│       └── styles.py        # التنسيقات
├── vendor/
│   └── ab/
│       └── windows/
│           └── ab.exe       # ملف ApacheBench
├── requirements.txt
├── run.bat
└── README.md
```

## ⚠️ تحذير

**استخدم هذه الأداة فقط على المواقع التي تملكها أو لديك إذن صريح لاختبارها!**

## 📄 الترخيص

يستخدم هذا التطبيق ApacheBench من مشروع Apache HTTP Server، مرخص بموجب Apache License 2.0.

</div>
