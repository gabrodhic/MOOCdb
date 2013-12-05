# encoding: UTF-8
# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20131204202312) do

  create_table "offerings", force: true do |t|
    t.string   "name"
    t.integer  "visualization_id"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "tags", force: true do |t|
    t.string "name"
  end

  create_table "uploads", force: true do |t|
    t.integer  "visualization_id"
    t.integer  "user_id"
    t.integer  "visualization_step_id"
    t.integer  "offering_id"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.string   "content_file_name"
    t.string   "content_content_type"
    t.integer  "content_file_size"
    t.datetime "content_updated_at"
  end

  create_table "user_sessions", force: true do |t|
    t.string   "user_session_id", null: false
    t.text     "date"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  add_index "user_sessions", ["updated_at"], name: "index_user_sessions_on_updated_at"
  add_index "user_sessions", ["user_session_id"], name: "index_user_sessions_on_user_session_id"

  create_table "users", force: true do |t|
    t.string   "username"
    t.string   "email"
    t.string   "crypted_password"
    t.string   "password_salt"
    t.string   "persistence_token"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "visualization_steps", force: true do |t|
    t.string   "name"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "visualization_types", force: true do |t|
    t.string   "name"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "visualizations", force: true do |t|
    t.string   "name"
    t.integer  "visualization_type_id"
    t.integer  "user_id"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.string   "description"
    t.integer  "tag_id"
  end

end
