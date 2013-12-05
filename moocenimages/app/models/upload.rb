class Upload < ActiveRecord::Base
  attr_accessible :content, :visualization_id, :user_id, :visualization_step_id, :offering_id
  
  has_attached_file :content
  
  belongs_to :offering
end
