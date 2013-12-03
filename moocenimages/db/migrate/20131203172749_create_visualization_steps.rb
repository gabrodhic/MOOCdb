class CreateVisualizationSteps < ActiveRecord::Migration
  def change
    create_table :visualization_steps do |t|
    	t.string :name
    	t.timestamps
    end
  end
end
