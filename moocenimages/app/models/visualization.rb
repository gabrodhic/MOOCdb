class Visualization < ActiveRecord::Base
  attr_accessible :name, :visualization_type_id, :user_id, :description, :tag_id, :thumbnail

  has_attached_file :thumbnail

  belongs_to :user
  has_many :offerings
  belongs_to :tag
end
