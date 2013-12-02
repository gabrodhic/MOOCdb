class CreateUsersAndUserSessions < ActiveRecord::Migration
  def change
    create_table :users do |t|
    	t.string :username
    	t.string :email
    	t.string :crypted_password
    	t.string :password_salt
    	t.string :persistence_token

    	t.timestamps
    end

    create_table :user_sessions do |t|
      t.string :user_session_id, :null => false
      t.text :date
      t.timestamps
    end

    add_index :user_sessions, :user_session_id
    add_index :user_sessions, :updated_at
  end
end
