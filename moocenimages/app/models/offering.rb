class Offering < ActiveRecord::Base
	attr_accessible :name, :visualization_id

	has_many :uploads
end
