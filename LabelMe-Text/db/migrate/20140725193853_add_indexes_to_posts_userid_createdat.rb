class AddIndexesToPostsUseridCreatedat < ActiveRecord::Migration
  def change
    add_index :posts, [:author_id, :created_at]
  end
end
