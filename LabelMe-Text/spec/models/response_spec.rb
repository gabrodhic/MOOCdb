require 'rails_helper'

RSpec.describe Response, :type => :model do
  let(:user) { FactoryGirl.create(:user) }
  let(:post) { FactoryGirl.create(:post, user: user) }
  let(:sentence) { FactoryGirl.create(:sentence, post_id: post.id) }

  before { @response = user.responses.build(sentence_id: sentence.id, label: "content") }

  subject { @response }

  it { should respond_to(:user_id) }
  it { should respond_to(:sentence_id) }
  it { should respond_to(:label) }

  its(:user) { should eq user }

  it { should be_valid }

  describe "when label is not present" do
    before { @response.label = " " }
    it { should_not be_valid }
  end

  describe "when user is not present" do
    before { @response.user_id = nil }
    it { should_not be_valid }
  end

  describe "when sentence is not present" do
    before { @response.sentence_id = nil }
    it { should_not be_valid }
  end
end
