class AddContentToFiles < ActiveRecord::Migration
  def up
  	add_attachment :files, :content
  end

  def down
  	remove_attachment :files, :content
  end
end
