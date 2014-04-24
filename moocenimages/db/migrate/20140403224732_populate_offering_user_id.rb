class PopulateOfferingUserId < ActiveRecord::Migration
  def change
    Offering.all.each do |offering|
      if offering.user_id.nil?
        begin
          visualization = Visualization.find(offering.visualization_id)
          offering.user_id = visualization.user_id
          offering.save
        rescue ActiveRecord::RecordNotFound
          offering.destroy
        end
      end
    end
  end
end
