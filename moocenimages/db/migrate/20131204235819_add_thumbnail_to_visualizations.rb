class AddThumbnailToVisualizations < ActiveRecord::Migration
  def up
    add_attachment :visualizations, :thumbnail
  end

  def down
    remove_attachment :visualizations, :thumbnail
  end
end
