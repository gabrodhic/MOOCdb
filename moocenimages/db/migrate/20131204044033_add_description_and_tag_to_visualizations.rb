class AddDescriptionAndTagToVisualizations < ActiveRecord::Migration
  def change
  	add_column :visualizations, :description, :string
  	add_column :visualizations, :tag_id, :integer
  end
end
