# frozen_string_literal: true

assets = Rails.application.assets

paths = assets.each_file.filter_map do |filename|
  logical = assets.attributes_for(filename).logical_path
  logical if logical.start_with?("blacklight/") && logical.end_with?(".js")
end.uniq.sort

puts paths

