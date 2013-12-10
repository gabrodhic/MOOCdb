class RenameFilesAndDeleteFileTypeColumn < ActiveRecord::Migration
  def change
    rename_table :files, :uploads

    remove_column :uploads, :file_type
  end
end
