{{ fullname | escape | underline}}

=============================================
(:mod:`actual_module_name`)
=============================================

Brief description of what this module does and its purpose

.. automodule:: {{ folder_name }}

   {% block modules %}
   {% if modules %}
   .. rubric:: {{ _('Sub-folders') }}

   .. autosummary::
      :toctree:
   {% for item in modules %}
      {{ item }} -- Purpose of this sub-folder
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block functions %}
   {% if functions %}
   .. rubric:: {{ _('Functions') }}

   .. autosummary::
      :toctree:
   {% for item in functions %}
      {{ item }} -- What this function does
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block classes %}
   {% if classes %}
   .. rubric:: {{ _('Classes') }}

   .. autosummary::
      :toctree:
      :template: custom-class-template.rst
   {% for item in classes %}
      {{ item }} -- Purpose of this class
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block notes %}
   {% if notes %}
   .. rubric:: {{ _('Notes') }}

   .. autosummary::
      :toctree:
   {% for item in notes %}
      {{ item }} -- Any additional information about using this module
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block seealso %}
   {% if seealso %}
   .. rubric:: {{ _('See Also') }}

   .. autosummary::
      :toctree:
   {% for item in notes %}
      {{ item }} -- Related modules or external links
   {%- endfor %}
   {% endif %}
   {% endblock %}