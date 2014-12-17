class ChangeResponseContentToText < ActiveRecord::Migration
  def up
    change_column :responses, :label, :text
  end

  def down
    change_column :responses, :label, :string
  end
end
