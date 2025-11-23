# Django Template Syntax Rules - MANDATORY FOR ALL AI AGENTS

## ⚠️ CRITICAL: These rules are NON-NEGOTIABLE

Violating any of these rules will break the application. **DO NOT** modify Django templates without following these rules exactly.

---

## Rule 1: Comparison Operators MUST Have Spaces

Django's template parser **REQUIRES** spaces around all comparison operators.

### ✅ CORRECT Examples:
```django
{% if sort_by == 'itemName' %}
{% if status != 'active' %}
{% if count > 0 %}
{% if price <= 100 %}
{% if age >= 18 %}
{% if value < threshold %}
```

### ❌ WRONG Examples (These will cause TemplateSyntaxError):
```django
{% if sort_by=='itemName' %}          ← NO SPACES = SYNTAX ERROR
{% if status!='active' %}             ← NO SPACES = SYNTAX ERROR
{% if count>0 %}                      ← NO SPACES = SYNTAX ERROR
{% if price<=100 %}                   ← NO SPACES = SYNTAX ERROR
```

**Error Message You'll See:**
```
TemplateSyntaxError: Could not parse the remainder: '=='itemName''
Invalid block tag on line X: 'endif', expected 'endblock'
```

---

## Rule 2: Template Variables MUST Be On ONE Line

Django template tags `{{ }}` and `{% %}` **MUST NOT** be split across multiple lines.

### ✅ CORRECT Example:
```django
<span>{{ item.createdBy.get_full_name|default:item.createdBy.username }}</span>
```

### ❌ WRONG Example (Renders as literal text):
```django
<span>{{ 
    item.createdBy.get_full_name|default:item.createdBy.username 
}}</span>
```

**What Happens:**
- The browser will display: `{{ item.createdBy.get_full_name|default:item.createdBy.username }}`
- Instead of displaying: `John Doe` or the username

**Why It Breaks:**
- Django's template parser expects opening `{{` and closing `}}` on the same line
- Line breaks inside template tags cause Django to stop parsing and render as text

---

## Rule 3: DO NOT "Fix" Line Length By Breaking Template Tags

Long lines in templates are **acceptable** and **preferred** over broken functionality.

### Priority: Functionality > Readability

If you need to break a long line:
- ✅ Break **OUTSIDE** template tags `{{ }}` or `{% %}`
- ❌ DO NOT break **INSIDE** template tags

### ✅ CORRECT Example (breaking outside tags):
```django
<option value="{{ item.id }}" 
        data-name="{{ item.itemName }}" 
        data-sign="{{ item.sign|default:'' }}">
    {{ item.itemName }}{% if item.sign %} | {{ item.sign }}{% endif %}
</option>
```

### ❌ WRONG Example (breaking inside tags):
```django
<option value="{{ item.id }}" 
        data-name="{{ item.itemName }}" 
        data-sign="{{ item.sign|
                     default:'' }}">  ← BROKEN: Split {{ }} tag
    {{ item.itemName }}{% if item.sign %} | 
    {{ item.sign }}{% endif %}        ← BROKEN: Split {% %} tag
</option>
```

---

## How to Prevent These Issues

### For Human Developers:
1. **Never** manually format Django templates with auto-formatters (Prettier, Black, etc.)
2. **Always** keep template tags on one line, even if they exceed 80-120 character limits
3. **Always** add spaces around comparison operators: `==`, `!=`, `<`, `>`, `<=`, `>=`
4. Use linters that understand Django template syntax (django-html)

### For AI Agents:
1. **SCAN** all Django templates (files in `templates/**/*.html`) before modifying
2. **VERIFY** every `{% if %}` statement has spaces around operators
3. **CHECK** that no `{{ }}` or `{% %}` tags are split across lines
4. **READ** this file (`DJANGO_TEMPLATE_RULES.md`) before any template modifications
5. **NEVER** prioritize code style over functionality in templates

---

## Files With Protection Comments

The following files have AI-prevention comments at the top. **READ THEM** before editing:

- `core/templates/core/items/list.html`
- `core/templates/core/items/detail.html`
- `core/templates/core/inventory/list.html`
- `core/templates/core/inventory/store_detail.html`

---

## Testing After Template Changes

Always test the page after modifying templates:

```bash
# Run the development server
python manage.py runserver

# Visit the affected pages:
# http://localhost:8000/items/
# http://localhost:8000/items/<id>/
# http://localhost:8000/inventory/
# http://localhost:8000/inventory/store/<id>/
```

If you see:
- `TemplateSyntaxError` → Check for missing spaces around operators
- Raw template code `{{ ... }}` displayed → Check for split template tags

---

## Summary

| Rule | Requirement | Impact if Violated |
|------|------------|-------------------|
| **Operator Spacing** | MUST have spaces: `{% if x == 'y' %}` | TemplateSyntaxError, page crash |
| **One-Line Tags** | `{{ }}` and `{% %}` on ONE line | Renders as text, not evaluated |
| **No Breaking Tags** | Break lines OUTSIDE tags only | Syntax errors or text display |

---

## Questions?

If you're an AI agent and unsure about a template modification:
1. ✅ Search for similar patterns in existing templates
2. ✅ Verify your changes won't split template tags
3. ✅ Check all comparison operators have spaces
4. ❌ DO NOT guess or assume - these rules are absolute

**Remember: A long line that works is better than a pretty line that breaks the application.**
