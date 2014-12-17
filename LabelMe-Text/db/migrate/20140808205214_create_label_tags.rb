class CreateLabelTags < ActiveRecord::Migration
  def change
    create_table :label_tags do |t|
      t.integer :label_category_id
      t.string :content
      
      t.timestamps
    end
  end
end
