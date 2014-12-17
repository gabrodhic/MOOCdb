class CreateUploads < ActiveRecord::Migration
  def change
    create_table :uploads do |t|
      t.attachment :csv
      t.boolean :header
      t.string :user_id

      t.timestamps
    end
  end
end
