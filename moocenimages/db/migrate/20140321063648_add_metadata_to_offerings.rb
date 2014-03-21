class AddMetadataToOfferings < ActiveRecord::Migration
  def change
    add_column :offerings, :platform, :string, :default => nil
    add_column :offerings, :instructor, :string, :default => nil
    add_column :offerings, :start_date, :date, :default => nil
    add_column :offerings, :end_date, :date, :default => nil
  end
end
