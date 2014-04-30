class Offering < ActiveRecord::Base
	attr_accessible :name, :visualization_id, :platform, :instructor, :start_date, :end_date, :user_id, :public_data

  has_attached_file :public_data,
                    :url => "/system/:class/:attachment/:id/:filename",
                    :path => ":rails_root/public:url"

  belongs_to :user, :foreign_key => :user_id
  belongs_to :visualization, :foreign_key => :visualization_id

  private

  Paperclip.interpolates :id  do |attachment, style|
    attachment.instance.id
  end
end
