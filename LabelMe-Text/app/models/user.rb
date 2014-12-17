class User < ActiveRecord::Base
  has_and_belongs_to_many :posts
  has_many :responses
  has_many :uploads, :dependent => :destroy
  before_save { self.email ? self.email = email.downcase : next }
  before_create :create_remember_token

  validates :name, presence: true, length: { maximum: 50 }, allow_blank: true
  VALID_EMAIL_REGEX = /\A[\w+\-.]+@[a-z\d\-.]+\.[a-z]+\z/i
  validates :email, presence: true, format: { with: VALID_EMAIL_REGEX },
                    uniqueness: { case_sensitive: false }, unless: :guest?

  has_secure_password(validations: false)
  validates :password, length: { minimum: 6 }, unless: :guest?
  validates :password_digest, presence: true, unless: :guest?
  validates :tos_agreement, presence: true

  def self.new_guest
    new { |u| u.guest = true; u.tos_agreement = true }
  end

  def display_name
    guest ? "Guest" : name
  end

  def User.new_remember_token
    SecureRandom.urlsafe_base64
  end

  def User.digest(token)
    Digest::SHA1.hexdigest(token.to_s)
  end

  def get_post_and_sentence
    while true
      if self.current_upload == nil
        post = nil
        sentence = nil
        return post, sentence
      end
      # if no post in current_post
      if self.current_post == nil
        #Pick a random post from the current upload
        upload_post_ids = Upload.find(current_upload).post_ids
        rand_id = rand(upload_post_ids.length)
        #Loop while we look for an available post
        responded_posts = self.post_ids

        # if we haven't finished responding to any posts, good
        if responded_posts == []
          post = Post.find(upload_post_ids[rand_id])
        # otherwise look for another post to use
        else
          post = search_for_post(responded_posts, rand_id)
        end
        
        # if no posts left to label, break out of the loop
        if post == nil
          sentence = nil
          return post, sentence
        end
        #set current_post to be post
        self.update_column(:current_post, "#{post.id}:0")
      else
        post = Post.find(self.current_post.split(":")[0])
      end

      # grab the sentence from self.current_post
      sent_array = post.sentence_ids
      sent_id = self.current_post.split(":")[1].to_i
      puts self.current_post
      if sent_id >= sent_array.length
        self.posts<<(post)
        self.current_post = nil
        next
      end
      sentence = Sentence.find(sent_array[sent_id])
      return post, sentence
    end
  end

  def search_for_post(post_ids, index)
    upload_post_ids = Upload.find(current_upload).post_ids
    post = Post.first(:conditions => [ "id >= ? AND id not IN (?) AND id IN (?)", index, post_ids, upload_post_ids])
    if post == nil
      post = Post.first(:conditions => [ "id <= ? AND id not IN (?) AND id IN (?)", index, post_ids, upload_post_ids])
      if post == nil
      return nil
      end
    return post
    end
  return post
  end

  def set_current_post_to_next_sentence
    old_post = self.current_post.split(":")
    self.update_column(:current_post, old_post[0] + ":" + "#{old_post[1].to_i+1}")
  end

  def get_post
    return Post.find(self.current_post.split(":")[0])
  end

  def clear_current_post
    self.update_column(:current_post, nil)
  end

  private

    def create_remember_token
      self.remember_token = User.digest(User.new_remember_token)
    end

    def set_current_upload(upload)
      self.update_column(:current_upload, upload)
    end
end
