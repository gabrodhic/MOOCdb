class CreateLabelCategories < ActiveRecord::Migration
  def change
    create_table :label_categories do |t|
      t.integer :upload_id
      t.string :content

      t.timestamps
    end
  end
end
