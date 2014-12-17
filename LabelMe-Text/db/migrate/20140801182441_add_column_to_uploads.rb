class AddColumnToUploads < ActiveRecord::Migration
  def change
    add_column :uploads, :column, :int 
  end
end
