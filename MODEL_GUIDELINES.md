"""
Django Model Field Guidelines for Tantawy Project
=================================================

Follow these patterns when creating new models to ensure proper NULL handling:

REQUIRED FIELDS (Don't use null=True):
- name = models.CharField(max_length=255)
- email = models.EmailField()
- price = models.DecimalField(max_digits=10, decimal_places=2)

OPTIONAL TEXT FIELDS (Use both null=True and blank=True):
- description = models.TextField(null=True, blank=True)
- notes = models.TextField(null=True, blank=True)
- comments = models.CharField(max_length=500, null=True, blank=True)

OPTIONAL FOREIGN KEYS (Use both null=True and blank=True):
- category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
- parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

OPTIONAL NUMERIC FIELDS (Use both null=True and blank=True):
- discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
- quantity = models.IntegerField(null=True, blank=True)

CHOICE FIELDS WITH DEFAULTS (Usually don't need null=True):
- status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)
- type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='active')

BOOLEAN FIELDS (Use default, not null=True):
- is_active = models.BooleanField(default=True)
- is_featured = models.BooleanField(default=False)

AUDIT FIELDS (Automatically inherited from BaseModel):
- createdAt, updatedAt, deletedAt  # DateTime fields
- createdBy, updatedBy, deletedBy  # User foreign keys
- isDeleted                        # Boolean field

REMEMBER:
- null=True = Allows NULL in database
- blank=True = Allows empty in forms/admin
- For optional fields, use BOTH null=True AND blank=True
- Audit fields are inherited automatically from BaseModel
- Always inherit from BaseModel for consistent audit trail
"""