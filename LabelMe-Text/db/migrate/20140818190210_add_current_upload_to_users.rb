class AddCurrentUploadToUsers < ActiveRecord::Migration
  def change
    add_column :users, :current_upload, :text
  end
end
