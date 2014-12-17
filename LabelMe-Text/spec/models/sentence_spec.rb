require 'rails_helper'

RSpec.describe Sentence, :type => :model do

  let(:user) { FactoryGirl.create(:user) }
  let(:post) { FactoryGirl.create(:post, user: user) }

  before { @sentence = post.sentences.build(content: "The quick brown fox jumped.") }

  subject { @sentence }

  it { should respond_to :content }
  it { should respond_to :post_id }
  it { should respond_to :post }
  its(:post) { should eq post }

  it { should be_valid }

  describe "post_id is not present" do
    before { @sentence.post_id = nil }
    it { should_not be_valid }
  end

end
