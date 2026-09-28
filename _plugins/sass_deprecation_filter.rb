# frozen_string_literal: true

# Minimal Mistakes 4.x requires Sass @import entry points. Silence only that
# known upstream deprecation until the theme migrates to the module system.
module SassDeprecationFilter
  private

  def sass_configs
    super.merge(:silence_deprecations => ["import"])
  end
end

Jekyll::Converters::Scss.prepend(SassDeprecationFilter)
