class CreateSentences < ActiveRecord::Migration
  def change
    create_table :sentences do |t|
      t.string :content
      t.integer :post_id

      t.timestamps
    end
    add_index :sentences, [:post_id]
  end
end
