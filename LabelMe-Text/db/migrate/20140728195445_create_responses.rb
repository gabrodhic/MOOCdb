class CreateResponses < ActiveRecord::Migration
  def change
    create_table :responses do |t|
      t.integer :user_id
      t.integer :sentence_id
      t.string :label

      t.timestamps
    end
    add_index :responses, [:user_id, :sentence_id]
  end
end
