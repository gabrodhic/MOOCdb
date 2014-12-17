class ChangeAuthorIdToUploadId < ActiveRecord::Migration
  def change
    rename_column :posts, :author_id, :upload_id
  end
end
