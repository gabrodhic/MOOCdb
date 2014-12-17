class AddInstructionsToUploads < ActiveRecord::Migration
  def change
    add_column :uploads, :instructions, :text 
  end
end
