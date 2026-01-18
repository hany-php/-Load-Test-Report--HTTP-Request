# -*- coding: utf-8 -*-
"""
النصوص العربية لواجهة المستخدم
Arabic UI Texts with RTL Support
"""


class ArabicTexts:
    """جميع النصوص العربية للتطبيق"""

    # عنوان التطبيق
    APP_TITLE = "أداة اختبار الحمل"
    APP_SUBTITLE = "اختبار أداء المواقع باستخدام ApacheBench"

    # تحذير
    WARNING_MESSAGE = "⚠️ تحذير: استخدم هذه الأداة فقط على المواقع التي تملكها أو لديك إذن صريح لاختبارها!"

    # قسم الإدخال
    INPUT_SECTION = "إعدادات الاختبار"
    URL_LABEL = "رابط الموقع:"
    URL_PLACEHOLDER = "https://example.com/"
    TOTAL_REQUESTS_LABEL = "إجمالي الطلبات (-n):"
    CONCURRENT_REQUESTS_LABEL = "التزامن (-c):"
    KEEP_ALIVE_LABEL = "تفعيل Keep-Alive (-k)"
    KEEP_ALIVE_TOOLTIP = "استخدام ميزة HTTP Keep-Alive للاتصالات المستمرة"

    # الأزرار
    BTN_START = "▶ بدء الاختبار"
    BTN_STOP = "■ إيقاف"
    BTN_RUNNING = "⏳ جاري التنفيذ..."
    BTN_COPY = "📋 نسخ"
    BTN_EXPORT_JSON = "💾 تصدير JSON"
    BTN_EXPORT_TXT = "📝 تصدير TXT"
    BTN_EXPORT_PDF = "📑 تصدير PDF"
    BTN_CLEAR = "🗑️ مسح"
    BTN_COPIED = "✓ تم النسخ!"

    # التبويبات
    TAB_RAW_OUTPUT = "📄 المخرجات الخام"
    TAB_SUMMARY = "📊 الملخص"

    # رسائل placeholder
    PLACEHOLDER_RAW = "ستظهر المخرجات هنا...\n\nقم بتكوين الاختبار واضغط 'بدء الاختبار' للبدء."
    PLACEHOLDER_SUMMARY = "سيظهر ملخص الاختبار هنا بعد اكتمال الاختبار..."

    # حدود
    LIMITS_FORMAT = "الحدود القصوى: {requests:,} طلب، {concurrency} متزامن"

    # القوائم
    MENU_FILE = "ملف"
    MENU_SETTINGS = "إعدادات"
    MENU_HELP = "مساعدة"

    MENU_EXPORT_JSON = "تصدير كـ JSON..."
    MENU_EXPORT_TXT = "تصدير كـ TXT..."
    MENU_EXPORT_PDF = "تصدير كـ PDF..."
    MENU_EXIT = "خروج"

    MENU_ADVANCED = "إعدادات متقدمة..."

    MENU_ABOUT = "حول التطبيق"
    MENU_CHECK_AB = "فحص تثبيت ApacheBench"

    # مربعات الإعدادات المتقدمة
    DIALOG_ADVANCED_TITLE = "إعدادات متقدمة"
    DIALOG_MAX_REQUESTS = "أقصى عدد طلبات:"
    DIALOG_MAX_CONCURRENCY = "أقصى تزامن:"

    # رسائل الحالة
    STATUS_READY = "جاهز. قم بتكوين الاختبار واضغط بدء."
    STATUS_TESTING = "جاري اختبار {url}..."
    STATUS_STOPPING = "جاري الإيقاف..."
    STATUS_SUCCESS = "✓ اكتمل الاختبار بنجاح!"
    STATUS_FAILED = "✗ فشل الاختبار: {error}"
    STATUS_CANCELLED = "✗ تم إلغاء أو فشل الاختبار."
    STATUS_AB_FOUND = "✓ تم العثور على ApacheBench: {path}"
    STATUS_AB_NOT_FOUND = "⚠️ لم يتم العثور على ApacheBench!"

    # رسائل الأخطاء
    ERROR_INVALID_URL = "الرابط يجب أن يبدأ بـ http:// أو https://"
    ERROR_INVALID_URL_TITLE = "رابط غير صالح"
    ERROR_CONCURRENCY = "التزامن لا يمكن أن يتجاوز إجمالي الطلبات."
    ERROR_CONCURRENCY_TITLE = "تكوين غير صالح"
    ERROR_CONFIG_TITLE = "تكوين غير صالح"
    ERROR_AB_NOT_FOUND_TITLE = "لم يتم العثور على ApacheBench"
    ERROR_AB_NOT_FOUND_MSG = "ApacheBench (ab) غير مكوّن بشكل صحيح.\n\n{message}"
    ERROR_EXPORT_TITLE = "فشل التصدير"
    ERROR_EXPORT_MSG = "حدث خطأ أثناء التصدير:\n{error}"

    # رسائل النجاح
    SUCCESS_EXPORT_TITLE = "تم التصدير"
    SUCCESS_EXPORT_MSG = "تم تصدير النتائج إلى:\n{filepath}"

    # مربع حوار الخروج
    CONFIRM_EXIT_TITLE = "اختبار قيد التشغيل"
    CONFIRM_EXIT_MSG = "يوجد اختبار قيد التشغيل. هل تريد إيقافه والخروج؟"

    # مربع حوار عن التطبيق
    ABOUT_TITLE = "حول أداة اختبار الحمل"
    ABOUT_CONTENT = """
    <h2 style='text-align: center;'>أداة اختبار الحمل</h2>
    <p style='text-align: center;'>واجهة رسومية لأداة ApacheBench (ab)</p>
    <p style='text-align: center;'>الإصدار 1.0.0</p>
    <hr>
    <p style='text-align: center;'>يستخدم هذا التطبيق ApacheBench من مشروع Apache HTTP Server،
    مرخص بموجب Apache License 2.0.</p>
    <p style='text-align: center;'>انظر THIRD_PARTY_NOTICES.txt لمعلومات الترخيص.</p>
    """

    # ملخص النتائج
    SUMMARY_TITLE = "ملخص نتائج الاختبار"
    SUMMARY_SERVER_INFO = "معلومات الخادم"
    SUMMARY_SERVER = "الخادم:"
    SUMMARY_HOST = "المضيف:"
    SUMMARY_DOC_PATH = "مسار المستند:"
    SUMMARY_DOC_LENGTH = "طول المستند:"

    SUMMARY_PERFORMANCE = "الأداء"
    SUMMARY_REQUESTS_PER_SEC = "الطلبات/ثانية:"
    SUMMARY_TIME_PER_REQUEST = "زمن/طلب (متوسط):"
    SUMMARY_TRANSFER_RATE = "معدل النقل:"
    SUMMARY_TOTAL_TIME = "الزمن الإجمالي:"

    SUMMARY_REQUESTS = "إحصائيات الطلبات"
    SUMMARY_COMPLETE = "طلبات مكتملة:"
    SUMMARY_FAILED = "طلبات فاشلة:"
    SUMMARY_CONCURRENCY = "مستوى التزامن:"
    SUMMARY_TOTAL_TRANSFERRED = "إجمالي المنقول:"
    SUMMARY_HTML_TRANSFERRED = "HTML المنقول:"

    SUMMARY_RESPONSE_TIMES = "أزمنة الاستجابة (مللي ثانية)"
    SUMMARY_MIN = "أدنى"
    SUMMARY_MEAN = "متوسط"
    SUMMARY_MEDIAN = "الوسيط"
    SUMMARY_MAX = "أقصى"
    SUMMARY_CONNECT = "الاتصال:"
    SUMMARY_PROCESSING = "المعالجة:"
    SUMMARY_WAITING = "الانتظار:"
    SUMMARY_TOTAL = "الإجمالي:"

    SUMMARY_PERCENTILES = "النسب المئوية (مللي ثانية)"
    SUMMARY_PERCENTILE_FORMAT = "{percent}% من الطلبات اكتملت في"

    SUMMARY_NOT_AVAILABLE = "غير متاح"
    SUMMARY_BYTES = "بايت"
    SUMMARY_KB_SEC = "ك.ب/ث"
    SUMMARY_MS = "م.ث"
    SUMMARY_SEC = "ث"
    SUMMARY_REQ_SEC = "طلب/ث"
