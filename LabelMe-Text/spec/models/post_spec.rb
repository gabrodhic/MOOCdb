require 'rails_helper'

RSpec.describe Post, :type => :model do
  let(:user) { FactoryGirl.create(:user) }
  before { @post = user.posts.build(content: "Here's a sentence.") }

  subject { @post }

  it { should respond_to(:content) }
  it { should respond_to(:user_id) }
  it { should respond_to(:user) }
  its(:user) { should eq user}

  it { should be_valid } 

  describe "when user_id is not present" do
    before { @post.user_id = nil }
    it { should_not be_valid }
  end

  describe "with blank content" do
    before { @post.content = " " }
    it { should_not be_valid }
  end

  describe "to sentence method" do
    let!(:longer_post) do
      FactoryGirl.create(:post, content: "Here's a few setences. They should be split up.", user: user)
    end

    let!(:no_punctuation) do
      FactoryGirl.create(:post, content: "Here's a few setences", user: user)
    end

    it "should generate sentences" do
      expect { longer_post.to_sentences }.to change(Sentence, :count).by(2)
    end

    it "should allow no punctuation/end of line" do
      expect { no_punctuation.to_sentences }.to change(Sentence, :count).by(1)
    end
  end
end
