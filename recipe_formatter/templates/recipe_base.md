[//]: # (Template for formatting recipes cleanly)

## {{recipe_name}}

### Yield: {{yields["servings"]}} servings

### Ingredients
{% for ingredient, spec in ingredients.items() %}
  - {{ingredient}}: {{spec['amounts']['amount']}} {{spec['amounts']['unit']}}
    {% if "notes" in spec %}
        {% for note in spec["notes"] %}
    - {{note}}
        {% endfor %}
    {% endif %}
{% endfor %}

### Steps
{% for step in steps %}
  - {{step}}
{% endfor %}
