class RefactorVisualizationAttachments < ActiveRecord::Migration
  def change
    add_attachment :visualizations, :data_extraction_script
    add_attachment :visualizations, :data_aggregation_script
    add_attachment :visualizations, :data_to_visualization_script

    add_attachment :offerings, :public_data

    add_column :offerings, :user_id, :integer
    add_index :offerings, :user_id

    Visualization.all.each do |visualization|
      uploads = Upload.where(:visualization_id => visualization.id)
      uploads.each do |upload|
        if upload.visualization_step_id == 2
          visualization.data_extraction_script = upload.content
        elsif upload.visualization_step_id == 4
          visualization.data_aggregation_script = upload.content
        elsif upload.visualization_step_id == 5
          offering = Offering.find(upload.offering_id)
          offering.public_data = upload.content
          offering.user_id = upload.user_id
          offering.save
        elsif upload.visualization_step_id == 6
          visualization.data_to_visualization_script = upload.content
        else
          raise ScriptError "visualization step id is not 2, 4, 5, or 6"
        end
      end
      visualization.save
    end

    drop_table :uploads
  end
end
