class CreateVisualizations < ActiveRecord::Migration
  def change
    create_table :visualizations do |t|
      t.string :name
      t.integer :visualization_type_id
      t.integer :user_id
      t.timestamps
    end
  end
end
