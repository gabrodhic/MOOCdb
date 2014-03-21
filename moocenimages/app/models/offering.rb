class Offering < ActiveRecord::Base
	attr_accessible :name, :visualization_id, :platform, :instructor, :start_date, :end_date

	has_many :uploads
end
