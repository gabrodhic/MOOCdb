class CreateComments < ActiveRecord::Migration
  def change
    create_table :comments do |t|
      t.text :contents
      t.integer :user_id
      t.integer :parent_id

      t.timestamps
    end

    add_index :comments, :user_id
    add_index :comments, :parent_id

    # create join table for visualizations and comments
    create_join_table :visualizations, :comments do |t|
      t.index :visualization_id
      t.index :comment_id
    end

    # adding indexes for existing models
    add_index :offerings, :visualization_id
    add_index :offerings, :platform

    add_index :visualizations, :user_id
    add_index :visualizations, :tag_id
  end
end
