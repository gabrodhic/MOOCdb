class LabelCategory < ActiveRecord::Base
  belongs_to :upload
  has_many :label_tags, :dependent => :destroy
  accepts_nested_attributes_for :label_tags, :allow_destroy => true
  validates :label_tags, :presence => true
  validates :content, :presence => true
end
