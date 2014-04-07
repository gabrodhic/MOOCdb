class Offering < ActiveRecord::Base
	attr_accessible :name, :visualization_id, :platform, :instructor, :start_date, :end_date, :user_id

  has_attached_file :public_data,
                    :url => "/system/:class/:attachment/:id/:filename",
                    :path => ":rails_root/public:url"

  belongs_to :user

  private

  Paperclip.interpolates :id  do |attachment, style|
    attachment.instance.id
  end
end
