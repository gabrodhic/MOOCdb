class AddCurrentPostToUsers < ActiveRecord::Migration
  def change
    add_column :users, :current_post, :string
  end
end
