class Visualization < ActiveRecord::Base
	attr_accessible :name, :visualization_type_id, :user_id

	belongs_to :user
end
