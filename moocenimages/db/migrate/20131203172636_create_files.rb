class CreateFiles < ActiveRecord::Migration
  def change
    create_table :files do |t|
    	t.integer :visualization_id
    	t.integer :user_id
    	t.integer :visualization_step_id
    	t.integer :offering_id
    	t.integer :file_type
    	t.string :file_type

    	t.timestamps
    end
  end
end
