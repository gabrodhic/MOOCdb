class LabelTag < ActiveRecord::Base
  belongs_to :label_category
  validates :content, :presence => true
end
