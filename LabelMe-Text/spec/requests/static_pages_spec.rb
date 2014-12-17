require 'spec_helper'

describe "Static pages" do
include Rails.application.routes.url_helpers
  subject { page }

  describe "Home page" do
    before { visit root_path}

    it { should have_content('Label Site') } 
    it { should have_title("LabelSite") }
    it { should_not have_title("| Home") }
  end

  describe "Help page" do
    before {visit help_path}

    it { should have_content('Help') }
    it { should have_title("LabelSite | Help") }
  end

  describe "About page" do
    before {visit about_path}

    it { should have_content('About Us') }
    it { should have_title("LabelSite | About Us") }
  end

  describe "Contact page" do
    before {visit contact_path}
    it { should have_content('Contact') }
    it { should have_title("LabelSite | Contact") }
  end
end
