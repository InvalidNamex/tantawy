# نظام إدارة المخزون - Inventory Management System

## نظرة عامة

تم إضافة نظام إدارة المخزون الشامل الذي يسمح للمستخدمين المصرح لهم بإدارة المخزون عبر جميع المتاجر.

## المميزات

### 1. عرض قائمة المتاجر
- عرض جميع المتاجر مع:
  - عدد الأصناف في كل متجر
  - إجمالي المخزون في كل متجر
- واجهة مستخدم جذابة مع بطاقات تفاعلية

### 2. عرض تفاصيل المتجر
- عرض جميع الأصناف في المتجر المحدد
- عرض الكمية المتاحة لكل صنف
- إمكانية البحث في الأصناف
- تصنيف الكميات بالألوان:
  - أخضر: كمية متاحة
  - أصفر: كمية صفر
  - أحمر: كمية سالبة

### 3. إضافة كميات
- إضافة كميات للأصناف في المخزن
- يتم إنشاء فاتورة شراء تلقائياً:
  - السعر: 0
  - المورد: أول مورد متاح في النظام
  - نوع الفاتورة: شراء (1)

### 4. خصم كميات
- خصم كميات من الأصناف في المخزن
- يتم إنشاء فاتورة مرتجع شراء تلقائياً:
  - السعر: 0
  - المورد: أول مورد متاح في النظام
  - نوع الفاتورة: مرتجع شراء (3)

## الصلاحيات

### مجموعة StoreAdmins
تم إنشاء مجموعة مستخدمين جديدة: `StoreAdmins`

المستخدمون في هذه المجموعة أو المسؤولين (superusers) يمكنهم:
- عرض جميع المتاجر
- عرض تفاصيل المخزون لكل متجر
- إضافة كميات للمخزون
- خصم كميات من المخزون

## المسارات (URLs)

```
/inventory/                            - قائمة المتاجر
/inventory/store/<store_id>/          - تفاصيل متجر معين
/inventory/add-quantity/              - إضافة كمية (AJAX)
/inventory/deduct-quantity/           - خصم كمية (AJAX)
```

## الملفات المضافة/المعدلة

### الملفات الجديدة:
1. `core/templates/core/inventory/list.html` - صفحة قائمة المتاجر
2. `core/templates/core/inventory/store_detail.html` - صفحة تفاصيل المتجر
3. `core/migrations/0022_create_storeadmins_group.py` - Migration لإنشاء المجموعة
4. `setup_inventory.py` - سكريبت الإعداد

### الملفات المعدلة:
1. `core/views.py` - إضافة Views جديدة:
   - `inventory_management_view()`
   - `inventory_store_detail_view()`
   - `inventory_add_quantity_view()`
   - `inventory_deduct_quantity_view()`
   - `user_is_store_admin()` - دالة مساعدة

2. `core/urls.py` - إضافة المسارات الجديدة

3. `templates/base.html` - إضافة رابط "إدارة المخزون" في القائمة

## التثبيت والإعداد

### 1. تشغيل Migrations

```bash
python manage.py migrate
```

هذا سيقوم بإنشاء مجموعة `StoreAdmins` تلقائياً.

### 2. إضافة مستخدمين إلى مجموعة StoreAdmins

#### طريقة 1: Django Admin
1. اذهب إلى `/admin/`
2. Users → اختر المستخدم
3. في قسم Groups، أضف `StoreAdmins`
4. احفظ

#### طريقة 2: Django Shell
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User, Group

# احصل على المستخدم
user = User.objects.get(username='your_username')

# احصل على المجموعة
group = Group.objects.get(name='StoreAdmins')

# أضف المستخدم للمجموعة
user.groups.add(group)

print(f"✓ تم إضافة {user.username} إلى مجموعة StoreAdmins")
```

### 3. التحقق من وجود موردين

تأكد من وجود مورد واحد على الأقل في النظام:

```bash
python manage.py shell
```

```python
from core.models import CustomerVendor

# تحقق من الموردين
vendors = CustomerVendor.objects.filter(type__in=[2, 3], isDeleted=False)
print(f"عدد الموردين: {vendors.count()}")

# إنشاء مورد إذا لم يكن موجوداً
if vendors.count() == 0:
    vendor = CustomerVendor.objects.create(
        customerVendorName="مورد افتراضي",
        type=2,  # Vendor
        notes="تم إنشاؤه تلقائياً لنظام إدارة المخزون"
    )
    print("✓ تم إنشاء مورد افتراضي")
```

## الاستخدام

### للمستخدمين:

1. **الوصول إلى النظام:**
   - انقر على "إدارة المخزون" في القائمة العلوية
   - أو اذهب مباشرة إلى `/inventory/`

2. **عرض تفاصيل متجر:**
   - انقر على بطاقة المتجر المطلوب
   - ستظهر قائمة بجميع الأصناف والكميات

3. **إضافة كمية:**
   - انقر على زر "إضافة" بجانب الصنف
   - أدخل الكمية المطلوبة
   - انقر "إضافة"
   - سيتم تحديث الصفحة تلقائياً

4. **خصم كمية:**
   - انقر على زر "خصم" بجانب الصنف
   - أدخل الكمية المطلوبة
   - انقر "خصم"
   - سيتم تحديث الصفحة تلقائياً

5. **البحث:**
   - استخدم مربع البحث لإيجاد صنف معين
   - انقر "بحث"

## الأمان

- ✓ فقط المستخدمون في مجموعة `StoreAdmins` أو `superusers` يمكنهم الوصول
- ✓ جميع العمليات محمية بـ `@login_required`
- ✓ التحقق من الصلاحيات قبل كل عملية
- ✓ استخدام CSRF tokens في جميع طلبات POST
- ✓ Validation كامل للبيانات المدخلة

## الفواتير المنشأة

### فاتورة إضافة كمية:
```python
{
    'invoiceType': 1,  # Purchase
    'customerOrVendorID': first_vendor,
    'storeID': selected_store,
    'price': 0,
    'quantity': entered_quantity,
    'paymentType': 1,  # Cash
    'status': 0,  # Paid
    'notes': 'إضافة كمية للمخزون - {item_name}'
}
```

### فاتورة خصم كمية:
```python
{
    'invoiceType': 3,  # Return Purchase
    'customerOrVendorID': first_vendor,
    'storeID': selected_store,
    'price': 0,
    'quantity': entered_quantity,
    'paymentType': 1,  # Cash
    'status': 0,  # Paid
    'notes': 'خصم كمية من المخزون - {item_name}'
}
```

## استعلامات قاعدة البيانات

النظام يستخدم view `itemStock` الموجود مسبقاً:

```sql
CREATE OR REPLACE VIEW "itemStock" AS
SELECT 
    i.id AS id, 
    i."itemName" AS "itemName",
    i."isDeleted" AS "isDeleted",
    COALESCE(im."storeID_id", id."storeID_id") AS "storeID",
    COALESCE(SUM(
        CASE 
            WHEN im."invoiceType" IN (1, 4) AND im."isDeleted" = FALSE THEN id.quantity 
            ELSE 0 
        END
    ), 0) 
    - 
    COALESCE(SUM(
        CASE 
            WHEN im."invoiceType" IN (2, 3) AND im."isDeleted" = FALSE THEN id.quantity 
            ELSE 0 
        END
    ), 0) AS stock
FROM items i
LEFT JOIN "invoiceDetail" id ON i.id = id.item_id
LEFT JOIN "invoiceMaster" im ON id."invoiceMasterID_id" = im.id
GROUP BY i.id, i."itemName", i."isDeleted", COALESCE(im."storeID_id", id."storeID_id");
```

## الأخطاء الشائعة وحلولها

### 1. خطأ: "لا يوجد موردين متاحين في النظام"
**الحل:** قم بإنشاء مورد واحد على الأقل (انظر قسم التثبيت والإعداد)

### 2. خطأ: "ليس لديك صلاحية الوصول لإدارة المخزون"
**الحل:** تأكد من إضافة المستخدم لمجموعة `StoreAdmins`

### 3. لا يظهر رابط "إدارة المخزون" في القائمة
**الحل:** 
- تأكد من تسجيل الدخول
- تأكد من أنك في مجموعة `StoreAdmins` أو `superuser`

### 4. خطأ عند إضافة/خصم كمية
**الحل:**
- تأكد من صحة الكمية المدخلة (رقم موجب)
- تأكد من وجود اتصال بالإنترنت
- تحقق من console المتصفح للأخطاء

## التحديثات المستقبلية المقترحة

1. ✨ إضافة إمكانية تصدير التقارير
2. ✨ إضافة إشعارات عند انخفاض المخزون
3. ✨ إضافة تاريخ لجميع التغييرات
4. ✨ إضافة إحصائيات وتحليلات
5. ✨ إضافة إمكانية نقل البضائع بين المخازن
6. ✨ إضافة صلاحيات أكثر تفصيلاً
7. ✨ إضافة API للهواتف المحمولة

## الدعم الفني

إذا واجهت أي مشاكل:
1. تحقق من logs Django
2. تحقق من console المتصفح
3. تأكد من صحة الصلاحيات
4. تأكد من تشغيل جميع Migrations

## الخلاصة

نظام إدارة المخزون جاهز للاستخدام! يوفر واجهة بسيطة وسهلة لإدارة المخزون عبر جميع المتاجر مع حفظ سجل كامل لجميع العمليات من خلال نظام الفواتير.
