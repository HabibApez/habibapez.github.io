# frozen_string_literal: true

require "cgi"
require "pathname"
require "uri"

site = Pathname.new(ARGV.fetch(0, "_site")).expand_path
abort "Site directory not found: #{site}" unless site.directory?

broken = []
attribute_pattern = /(?:href|src)=["']([^"']+)["']/i

site.glob("**/*.html").each do |html_file|
  html_file.read.scan(attribute_pattern).flatten.each do |reference|
    next if reference.empty? || reference.start_with?("#", "//")

    uri = URI.parse(reference)
    next if uri.scheme || uri.host

    path = CGI.unescape(uri.path.to_s)
    next if path.empty?

    candidate = if path.start_with?("/")
                  site.join(path.delete_prefix("/"))
                else
                  html_file.dirname.join(path).cleanpath
                end

    valid = candidate.file? || candidate.join("index.html").file?
    valid ||= candidate.extname.empty? && Pathname.new("#{candidate}.html").file?
    broken << "#{html_file.relative_path_from(site)} -> #{reference}" unless valid
  rescue URI::InvalidURIError
    broken << "#{html_file.relative_path_from(site)} -> invalid URI: #{reference}"
  end
end

if broken.empty?
  puts "Internal link check passed."
else
  warn "Broken internal links:\n#{broken.uniq.sort.join("\n")}"
  exit 1
end
