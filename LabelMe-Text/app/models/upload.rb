class Upload < ActiveRecord::Base
  belongs_to :user
  has_many :posts
  has_many :label_categories, :dependent => :destroy
  accepts_nested_attributes_for :label_categories, :allow_destroy => true
  
  serialize :labels

  has_attached_file :csv
  validates_attachment  :csv, :presence => true, :file_name => { :matches => /\.csv\z/ }
  validates :name, :presence => true
  validates :label_categories, :presence => true
  validates :description, :presence => true
  validates :column, :presence => true
  validates :instructions, :presence => true
end
