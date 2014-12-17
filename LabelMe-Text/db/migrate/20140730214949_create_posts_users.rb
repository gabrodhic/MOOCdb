class CreatePostsUsers < ActiveRecord::Migration
  def change
    create_table :posts_users do |t|
      t.integer :user_id
      t.integer :post_id

      t.timestamps
    end
  end
end
