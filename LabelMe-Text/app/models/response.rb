class Response < ActiveRecord::Base
  belongs_to :user
  serialize :label
  
  validates :user_id, presence: true
  validates :sentence_id, presence: true
  validates :label, presence: true

end
